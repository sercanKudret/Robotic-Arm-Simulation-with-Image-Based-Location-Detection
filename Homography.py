import mujoco
import cv2
import numpy as np

class RealWorldVision:
    def __init__(self, model, data):
        self.model = model
        self.data = data
        self.homography_matrix = None
        self.calibrated = False
        self.world_points = np.array([
            [0.4, 0.4], 
            [-0.4, 0.4], 
            [-0.4, -0.4], 
            [0.4, -0.4]
        ], dtype=np.float32)
        self.colors = {
            'red': [(0, 70, 50, 10, 255, 255), (160, 70, 50, 179, 255, 255)],
            'green': [(40, 50, 50, 80, 255, 255)],
            'blue': [(100, 50, 50, 130, 255, 255)],
            'yellow': [(20, 100, 100, 30, 255, 255)],
            'purple': [(125, 50, 50, 165, 255, 255)]
        }

    def get_image(self, camera="top_cam"):
        renderer = mujoco.Renderer(self.model, width=640, height=480)
        renderer.update_scene(self.data, camera=camera)
        rgb = renderer.render()
        bgr = cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)
        renderer.close()
        return bgr

    def find_color(self, image, color_name):
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        mask = np.zeros(hsv.shape[:2], dtype=np.uint8)
        for r in self.colors[color_name]:
            lower = np.array(r[:3])
            upper = np.array(r[3:])
            mask = cv2.bitwise_or(mask, cv2.inRange(hsv, lower, upper))
        mask = cv2.medianBlur(mask, 5)
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if contours:
            largest = max(contours, key=cv2.contourArea)
            if cv2.contourArea(largest) > 50:
                M = cv2.moments(largest)
                if M["m00"] > 0:
                    return (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
        return None

    def calibrate(self):
        image = self.get_image()
        image_points = []
        for color in ['red', 'green', 'blue', 'yellow']:
            point = self.find_color(image, color)
            if point:
                image_points.append(point)
                cv2.circle(image, point, 10, (16, 25, 53), 2)
                print(f"{color} nokta tespit edildi: {point}")
                cv2.putText(image, f"{color} Point", (point[0]+10, point[1]-10), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (16, 25, 53), 1)
            else:
                print(f"HATA: {color} bulunamadı!")
                return False
        cv2.imshow("Kalibrasyon", image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        if len(image_points) == 4:
            self.homography_matrix, _ = cv2.findHomography(
                np.array(image_points, dtype=np.float32), self.world_points)
            self.calibrated = True
            return True
        return False

    def pixel_to_world(self, x, y, z=0.02):
        if not self.calibrated:
            return None
        pixel = np.array([[[x, y]]], dtype=np.float32)
        world_2d = cv2.perspectiveTransform(pixel, self.homography_matrix)
        scale = (2.0 - z) / 2.0
        wx = world_2d[0][0][0] * scale
        wy = world_2d[0][0][1] * scale

        new_x = -wy
        new_y = -0.055 + z # 0.05 rolling base parçasının yerden yüksekliği
        new_z = -wx

        return (new_x, new_y, new_z)

    def detect_target(self, z=0.02):
        image = self.get_image()
        point = self.find_color(image, 'purple')
        if point:
            world_coords = self.pixel_to_world(point[0], point[1], z)
            cv2.circle(image, point, 10, (0, 255, 0), 2)
            cv2.putText(image, f"({world_coords[0]:.2f}, {world_coords[1]:.2f}, {world_coords[2]:.2f})",
                (point[0]+10, point[1]-10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
            cv2.imshow("Hedef", image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            return world_coords
        cv2.imshow("Hedef", image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        return None