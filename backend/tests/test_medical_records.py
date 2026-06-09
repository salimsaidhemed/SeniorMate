from io import BytesIO


def create_patient(client, **overrides):
    payload = {
        "first_name": "Maria",
        "last_name": "Santos",
    }
    payload.update(overrides)
    return client.post("/api/patients", json=payload).get_json()["data"]


def upload_payload(patient_id=None, include_file=True, **overrides):
    payload = {
        "title": "Updated care plan",
        "description": "Clinical plan for the next certification period.",
        "record_type": "care_plan",
        "uploaded_by": "Jordan Lee",
    }
    if patient_id is not None:
        payload["patient_id"] = str(patient_id)
    if include_file:
        payload["file"] = (
            BytesIO(b"%PDF-1.4 test medical record"),
            "care-plan.pdf",
            "application/pdf",
        )
    payload.update(overrides)
    return payload


def upload_record(client, patient_id, **overrides):
    return client.post(
        "/api/medical-records",
        data=upload_payload(patient_id, **overrides),
        content_type="multipart/form-data",
    )


def test_upload_medical_record_stores_metadata_and_object(
    client,
    medical_record_storage,
):
    patient = create_patient(client)

    response = upload_record(client, patient["id"])
    body = response.get_json()

    assert response.status_code == 201
    assert body["message"] == "Medical record uploaded successfully"
    assert body["data"]["patient_id"] == patient["id"]
    assert body["data"]["file_name"] == "care-plan.pdf"
    assert body["data"]["file_mime_type"] == "application/pdf"
    assert body["data"]["storage_bucket"] == medical_record_storage.bucket
    assert body["data"]["storage_object_key"] in medical_record_storage.objects


def test_list_medical_records(client):
    patient = create_patient(client)
    upload_record(client, patient["id"])

    response = client.get("/api/medical-records")

    assert response.status_code == 200
    assert len(response.get_json()["data"]) == 1


def test_list_medical_records_for_patient(client):
    patient = create_patient(client)
    other_patient = create_patient(client, first_name="John", last_name="Rivera")
    upload_record(client, patient["id"])
    upload_record(client, other_patient["id"], title="Assessment")

    response = client.get(f"/api/patients/{patient['id']}/medical-records")
    body = response.get_json()

    assert response.status_code == 200
    assert len(body["data"]) == 1
    assert body["data"][0]["patient_id"] == patient["id"]


def test_get_medical_record(client):
    patient = create_patient(client)
    created = upload_record(client, patient["id"]).get_json()["data"]

    response = client.get(f"/api/medical-records/{created['id']}")

    assert response.status_code == 200
    assert response.get_json()["data"]["title"] == "Updated care plan"


def test_update_medical_record_metadata(client):
    patient = create_patient(client)
    created = upload_record(client, patient["id"]).get_json()["data"]

    response = client.put(
        f"/api/medical-records/{created['id']}",
        json={
            "title": "Signed care plan",
            "record_type": "signed_care_plan",
            "uploaded_by": "Taylor Morgan",
        },
    )
    body = response.get_json()

    assert response.status_code == 200
    assert body["data"]["title"] == "Signed care plan"
    assert body["data"]["record_type"] == "signed_care_plan"
    assert body["data"]["file_name"] == "care-plan.pdf"


def test_download_medical_record_streams_private_object(client):
    patient = create_patient(client)
    created = upload_record(client, patient["id"]).get_json()["data"]

    response = client.get(f"/api/medical-records/{created['id']}/download")

    assert response.status_code == 200
    assert response.data == b"%PDF-1.4 test medical record"
    assert response.mimetype == "application/pdf"
    assert "care-plan.pdf" in response.headers["Content-Disposition"]


def test_delete_medical_record_removes_metadata_and_object(
    client,
    medical_record_storage,
):
    patient = create_patient(client)
    created = upload_record(client, patient["id"]).get_json()["data"]
    object_key = created["storage_object_key"]

    response = client.delete(f"/api/medical-records/{created['id']}")

    assert response.status_code == 200
    assert object_key not in medical_record_storage.objects
    assert client.get(f"/api/medical-records/{created['id']}").status_code == 404


def test_upload_requires_patient_id(client):
    response = client.post(
        "/api/medical-records",
        data=upload_payload(),
        content_type="multipart/form-data",
    )

    assert response.status_code == 400
    assert "patient_id" in response.get_json()["errors"]


def test_upload_requires_file(client):
    patient = create_patient(client)

    response = client.post(
        "/api/medical-records",
        data=upload_payload(patient["id"], include_file=False),
        content_type="multipart/form-data",
    )

    assert response.status_code == 400
    assert response.get_json()["errors"]["file"] == "This field is required."


def test_upload_rejects_invalid_patient_id(client):
    response = upload_record(client, 999)

    assert response.status_code == 400
    assert response.get_json()["errors"]["patient_id"] == "Patient not found."


def test_upload_rejects_unsupported_file_type(client):
    patient = create_patient(client)

    response = upload_record(
        client,
        patient["id"],
        file=(BytesIO(b"executable"), "malware.exe", "application/octet-stream"),
    )

    assert response.status_code == 400
    assert response.get_json()["errors"]["file"] == (
        "Use a PDF, JPEG, PNG, DOC, or DOCX file."
    )


def test_upload_rejects_file_with_mismatched_content(client):
    patient = create_patient(client)

    response = upload_record(
        client,
        patient["id"],
        file=(BytesIO(b"not actually a PDF"), "care-plan.pdf", "application/pdf"),
    )

    assert response.status_code == 400
    assert response.get_json()["errors"]["file"] == (
        "File content does not match the selected document type."
    )


def test_upload_rejects_file_over_configured_size(client):
    patient = create_patient(client)
    oversized_pdf = b"%PDF-" + (b"x" * (1024 * 1024))

    response = upload_record(
        client,
        patient["id"],
        file=(BytesIO(oversized_pdf), "large.pdf", "application/pdf"),
    )

    assert response.status_code == 400
    assert response.get_json()["errors"]["file"] == (
        "File size must not exceed 1 MB."
    )
