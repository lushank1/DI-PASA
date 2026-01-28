# DI-PASA
DI-PASA is a digital ergonomic risk assessment framework developed using Python and OpenCV for evaluating posture-related risks from static images. The method leverages image-based pose estimation to objectively quantify biomechanical parameters associated with risky occupational activities, particularly staircase ambulation.
The proposed approach enables the assessment of ergonomic risk directly from images, eliminating the need for wearable sensors or marker-based motion capture systems. 
By bounding a pose-estimation model (MediaPipe/OpenPose-based skeletal mapping) onto selected images, DI-PASA extracts anatomically relevant joint landmarks and reconstructs the human posture digitally. 
This allows the evaluation of postures observed during high-risk activities such as material handling, load carrying, load lifting, and different phases of the gait cycle, including swing and stance phases on staircases.

Using the detected skeletal model, DI-PASA computes critical joint angles—specifically trunk inclination, elbow flexion, and knee flexion—which are known indicators of musculoskeletal strain and balance demand. 
These joint angles are subsequently mapped to a three-level ergonomic risk classification (low, moderate, and high), enabling systematic identification of hazardous postures under varying task conditions and 
loading scenarios.

Compared to conventional ergonomic assessment techniques (e.g., observational checklists, questionnaire-based tools, or laboratory-dependent motion capture), DI-PASA offers several advantages. 
The method is non-invasive, low-cost, repeatable, and scalable, making it suitable for real-world industrial and occupational environments. 
Furthermore, the image-based nature of the framework allows retrospective analysis using recorded images or videos, providing greater flexibility than traditional assessment tools. 
Overall, DI-PASA presents an efficient digital alternative for posture-based ergonomic risk evaluation, particularly in complex tasks such as staircase ambulation with load handling.

<img width="1664" height="2604" alt="Material Handling Research Paper Flowchart" src="https://github.com/user-attachments/assets/6a3b5433-3804-4a9b-a00a-bf0cd439ef9d" />
