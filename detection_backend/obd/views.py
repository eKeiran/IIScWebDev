from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import cv2
import numpy as np
import base64
classes_path = "../yolov3.txt"  
with open(classes_path, 'r') as f:
    classes = [line.strip() for line in f.readlines()]
COLORS = np.random.uniform(0, 255, size=(len(classes), 3))
@csrf_exempt
def detect_objects(request):
    if request.method == 'POST' and request.FILES.get('image'):
        image_file = request.FILES['image']
        image_data = image_file.read()
        nparr = np.frombuffer(image_data, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        # Your object detection code here
        config_path = "../yolov3.cfg"  
        weights_path = "../yolov3.weights"  
        classes_path = "../yolov3.txt" 
        net = cv2.dnn.readNet(weights_path, config_path)

        Width = image.shape[1]
        Height = image.shape[0]
        scale = 0.00392

        blob = cv2.dnn.blobFromImage(image, scale, (416, 416), (0, 0, 0), True, crop=False)

        net.setInput(blob)

        outs = net.forward(get_output_layers(net))

        detected_objects = []
        class_ids = []
        confidences = []
        boxes = []
        conf_threshold = 0.5
        nms_threshold = 0.4
        class_count = {}
        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > 0.82:
                    center_x = int(detection[0] * Width)
                    center_y = int(detection[1] * Height)
                    w = int(detection[2] * Width)
                    h = int(detection[3] * Height)
                    x = center_x - w // 2
                    y = center_y - h // 2
                    detected_objects.append({
                        'class': classes[class_id],
                        'confidence': float(confidence),
                    })
                    class_ids.append(class_id)
                    boxes.append([x, y, w, h])
                    confidences.append(float(confidence))
                    class_count[classes[class_id]] = class_count.get(classes[class_id], 0) + 1
                    
        indices = cv2.dnn.NMSBoxes(boxes, confidences, conf_threshold, nms_threshold)
        for i in indices:
            try:
                box = boxes[i]
            except:
                i = i[0]
                box = boxes[i]
    
            x = box[0]
            y = box[1]
            w = box[2]
            h = box[3]
            draw_prediction(image, class_ids[i], confidences[i], round(x), round(y), round(x+w), round(y+h))
            
        _, processed_image_data = cv2.imencode('.jpg', image)
        processed_image_base64 = base64.b64encode(processed_image_data).decode('utf-8')
        total_objects_detected = len(detected_objects)
        response_data = {
            'total_objects_detected': total_objects_detected,
            'class_counts': class_count,
            'objects': detected_objects,
            'processed_image': processed_image_base64
        }
        # Return the processed image as a response
        return JsonResponse(response_data)

    else:
        return JsonResponse({'error': 'Invalid request'})

def get_output_layers(net):
    layer_names = net.getLayerNames()
    try:
        output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]
    except:
        output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
    return output_layers

def draw_prediction(img, class_id, confidence, x, y, x_plus_w, y_plus_h):
    classes_path = "../yolov3.txt"  
    with open(classes_path, 'r') as f:
        classes = [line.strip() for line in f.readlines()]
    
    COLORS = np.random.uniform(0, 255, size=(len(classes), 3))

    label = str(classes[class_id])
    
    color = COLORS[class_id]

    cv2.rectangle(img, (x,y), (x_plus_w,y_plus_h), color, 2)

    cv2.putText(img, label, (x-10,y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

