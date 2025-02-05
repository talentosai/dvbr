#!/bin/bash
gcloud config set project diversity-bridge-447208

for i in {0..49}
do
  gcloud compute addresses create mongo-ip-"$i" \
    --region=europe-west4 \
    --subnet=default
done

for i in {0..49}
do
  if [ "$(gcloud compute addresses describe mongo-ip-"$i" --region=europe-west4 --format="value(status)")" != "RESERVED" ]; then
    echo "mongo-ip-$i is not RESERVED";
    exit 1;
  fi
done

for i in {0..49}
do
  gcloud compute forwarding-rules create mongo-"$i" \
    --region=europe-west4 \
    --network=default \
    --address=mongo-ip-"$i" \
    --allow-psc-global-access \
    --target-service-attachment=projects/p-iprfmzv4nr6l7ymoeema6olv/regions/europe-west4/serviceAttachments/sa-europe-west4-67640ce05400bb2e8f733b81-"$i"
done

if [ "$(gcloud compute forwarding-rules list --regions=europe-west4 --format="csv[no-heading](name)" --filter="(name:mongo*)" | wc -l)" -gt 50 ]; then
  echo "Project has too many forwarding rules that match prefix mongo. Either delete the competing resources or choose another endpoint prefix."
  exit 2;
fi

gcloud compute forwarding-rules list --regions=europe-west4 --format="json(IPAddress,name)" --filter="name:(mongo*)" > atlasEndpoints-mongo.json
