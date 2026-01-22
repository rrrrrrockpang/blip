**ADDING CRONJOB**
---
apiVersion: batch/v1
kind: CronJob
metadata:
  name: monthly-data-update
spec:
  schedule: "0 0 1 * *"
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: data-updater
            image: gcr.io/blip-wild/fastapi-app:latest
            command: ["python", "app/05-encorp-new.py"]
            env:
            - name: TOGETHER_API_KEY
              valueFrom:
                secretKeyRef:
                  name: together-ai-secret
                  key: TOGETHER_API_KEY
          restartPolicy: OnFailure

Then run this:
kubectl apply -f your-file.yaml