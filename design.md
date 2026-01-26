```mermaid
graph TD
    %% --- STYLING ---
    classDef frontend fill:#e1f5fe,stroke:#01579b,stroke-width:2px;
    classDef backend fill:#fff3e0,stroke:#e65100,stroke-width:2px;
    classDef db fill:#e8f5e9,stroke:#1b5e20,stroke-width:2px;
    classDef ai fill:#f3e5f5,stroke:#4a148c,stroke-width:2px;
    classDef hardware fill:#eceff1,stroke:#37474f,stroke-width:2px;

    subgraph Zone_A_Client_Edge [Zone A: Client & Edge Layer]
        direction TB
        UI_Admin[React Admin Dashboard<br/>(Phase 4)]:::frontend
        UI_Reg[Smart Video Enrollment<br/>(Phase 4)]:::frontend
        
        subgraph Hardware_Edge [Phase 5: Edge Computing]
            Cam_RTSP[RTSP/IP Camera]:::hardware
            Pi_Node[Raspberry Pi 5<br/>Edge Detector]:::hardware
            YOLO_Edge[YOLOv8 Nano<br/>(Detection Only)]:::ai
        end
    end

    subgraph Zone_B_Core [Zone B: API & AI Logic]
        direction TB
        API[FastAPI Gateway]:::backend
        
        subgraph AI_Pipeline [AI Core Pipeline]
            YOLO_Server[YOLOv8 Server<br/>(Phase 2: Detection)]:::ai
            Recog_Engine[Face Recognition<br/>(ResNet/Dlib)]:::ai
            Liveness[Anti-Spoofing<br/>(Phase 3: Blink/Texture)]:::ai
        end

        subgraph Business_Logic [Phase 2: Logic Layer]
            State_Machine[Attendance State Machine<br/>(Check-In/Out Logic)]:::backend
            RBAC[RBAC Controller<br/>(Permissions)]:::backend
        end
    end

    subgraph Zone_C_Storage [Zone C: Data Layer]
        Postgres[(PostgreSQL DB<br/>Phase 1)]:::db
        S3_Bucket[(AWS S3 Bucket<br/>Images)]:::db
    end

    %% --- CONNECTIONS ---

    %% Flow 1: Smart Registration
    UI_Reg -- "1. Video Stream (Frames)" --> YOLO_Server
    YOLO_Server -- "2. Best 5 Frames" --> Recog_Engine
    Recog_Engine -- "3. Generate Embeddings" --> Postgres
    Recog_Engine -- "4. Save Photos" --> S3_Bucket

    %% Flow 2: Admin Actions
    UI_Admin -- "Fetch Reports/Logs" --> API
    API -- "Query Data" --> Postgres

    %% Flow 3: Edge Attendance (Phase 5)
    Cam_RTSP -- "RTSP Stream" --> Pi_Node
    Pi_Node -- "Run Detection" --> YOLO_Edge
    YOLO_Edge -- "Face Box + Metadata" --> API
    API -- "Verify Identity" --> Recog_Engine
    Recog_Engine -- "Match Found" --> State_Machine
    State_Machine -- "Log Attendance" --> Postgres

    %% Flow 4: Phase 2 Logic
    State_Machine -- "Check Rules (Dupes/Time)" --> Postgres
```