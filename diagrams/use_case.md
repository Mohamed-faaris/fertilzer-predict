```mermaid
usecaseDiagram
    actor User as "Farmer / User"
    actor System as "System"

    package "Fertilizer Prediction App" {
        usecase "View Dashboard" as UC1
        usecase "Analyze Crop Data" as UC2
        usecase "Analyze Soil Data" as UC3
        usecase "Get Single Recommendation" as UC4
        usecase "Get Batch Recommendations" as UC5
        usecase "Upload Valid CSV" as UC6
        usecase "View Reports" as UC7
        usecase "Interactive Visualizations" as UC8
    }

    User --> UC1
    User --> UC2
    User --> UC3
    User --> UC4
    User --> UC5
    User --> UC7
    User --> UC8

    UC5 ..> UC6 : <<include>>
    
    UC4 --> System : "Request Prediction"
    System --> UC4 : "Return Prediction & Confidence"
```
