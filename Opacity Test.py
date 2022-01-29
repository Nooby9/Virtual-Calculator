import cv2
import numpy as np

# Load image
img = cv2.VideoCapture(1).read()

# Initialize blank mask image of same dimensions for drawing the shapes
shapes = np.zeros_like(img, np.uint8)

# Draw shapes
cv2.rectangle(shapes, (5, 5), (100, 75), (255, 255, 255), cv2.FILLED)
cv2.circle(shapes, (300, 300), 75, (255, 255, 255), cv2.FILLED)

# Generate output by blending image with shapes image, using the shapes
# images also as mask to limit the blending to those parts
out = img.copy()
alpha = 0.5
mask = shapes.astype(bool)
out[mask] = cv2.addWeighted(img, alpha, shapes, 1 - alpha, 0)[mask]

# Visualization
cv2.imshow('Image', img)
cv2.imshow('Shapes', shapes)
cv2.imshow('Output', out)
cv2.waitKey(0)
cv2.destroyAllWindows()