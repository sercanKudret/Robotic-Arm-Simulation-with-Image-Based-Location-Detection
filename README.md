## Robotic Arm Simulation with Image Based Location Detection

This project features a custom-designed robotic arm simulated in the **MuJoCo physics engine**, with a fully self-implemented inverse kinematics algorithm using Python.

---

### 🛠️ Key Components

- 🧩 The arm's **STL parts** were sourced online and assembled in **FreeCAD**.  
- 📦 The merged model was exported and adapted into **MuJoCo's XML** format.  
- 🧠 A **custom inverse kinematics solver** was written in Python (no external IK libraries used), allowing the arm to reach any target **position (XYZ)** and **orientation (roll, pitch, yaw)**.

---

### 🧭 Scene Interaction & Object Localization

- 🎥 The environment contains an object detected using MuJoCo's **built-in camera**.  
- 📐 A **homography-based method** was used to estimate the object's position on the 2D image plane and convert it to **3D world coordinates**.  
- 📏 These coordinates were scaled according to the robot arm’s unit system and passed to the control pipeline.

---

### 🤖 Intelligent Positioning

- A **base-search approach** is used to find the first valid base rotation (omega) that allows the robot arm to reach the target.  
- The robot moves its end-effector to the desired world position and orientation based on the custom IK computation.

---

### 🔬 Highlights

- ✅ Fully custom inverse kinematics logic  
- ✅ Homography-based world position estimation  
- ✅ Real-time interaction with MuJoCo simulation  
- ✅ FreeCAD modeling and MuJoCo XML integration
