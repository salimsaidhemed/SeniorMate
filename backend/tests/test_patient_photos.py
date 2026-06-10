from io import BytesIO


PNG_BYTES = b"\x89PNG\r\n\x1a\nsynthetic-patient-photo"
JPEG_BYTES = b"\xff\xd8\xff\xe0synthetic-patient-photo"


def create_patient(client):
    return client.post(
        "/api/patients",
        json={"first_name": "Maria", "last_name": "Santos"},
    ).get_json()["data"]


def upload_photo(client, patient_id, content=PNG_BYTES, name="maria.png", mime="image/png"):
    return client.post(
        f"/api/patients/{patient_id}/photo",
        data={"file": (BytesIO(content), name, mime)},
        content_type="multipart/form-data",
    )


def test_patient_response_includes_photo_metadata(client):
    patient = create_patient(client)

    response = client.get(f"/api/patients/{patient['id']}")
    data = response.get_json()["data"]

    assert data["has_photo"] is False
    assert data["photo_verified"] is False
    assert data["photo_file_name"] is None
    assert data["photo_uploaded_at"] is None
    assert "photo_object_key" not in data


def test_upload_valid_patient_photo(client, patient_photo_storage):
    patient = create_patient(client)

    response = upload_photo(client, patient["id"])
    data = response.get_json()["data"]

    assert response.status_code == 201
    assert data["has_photo"] is True
    assert data["photo_verified"] is False
    assert data["photo_file_name"] == "maria.png"
    assert data["photo_uploaded_at"] is not None
    assert len(patient_photo_storage.objects) == 1
    object_key = next(iter(patient_photo_storage.objects))
    assert object_key.startswith(f"patients/{patient['id']}/profile/")


def test_get_patient_photo_streams_private_image(client):
    patient = create_patient(client)
    upload_photo(client, patient["id"])

    response = client.get(f"/api/patients/{patient['id']}/photo")

    assert response.status_code == 200
    assert response.data == PNG_BYTES
    assert response.mimetype == "image/png"
    assert response.headers["Content-Disposition"].startswith("inline;")


def test_upload_replaces_existing_photo(client, patient_photo_storage):
    patient = create_patient(client)
    upload_photo(client, patient["id"])
    previous_key = next(iter(patient_photo_storage.objects))

    response = upload_photo(
        client,
        patient["id"],
        content=JPEG_BYTES,
        name="replacement.jpg",
        mime="image/jpeg",
    )

    assert response.status_code == 201
    assert response.get_json()["data"]["photo_file_name"] == "replacement.jpg"
    assert previous_key not in patient_photo_storage.objects
    assert len(patient_photo_storage.objects) == 1


def test_upload_requires_file(client):
    patient = create_patient(client)

    response = client.post(
        f"/api/patients/{patient['id']}/photo",
        data={},
        content_type="multipart/form-data",
    )

    assert response.status_code == 400
    assert response.get_json()["errors"]["file"] == "This field is required."


def test_upload_rejects_invalid_mime_type(client):
    patient = create_patient(client)

    response = upload_photo(
        client,
        patient["id"],
        content=b"not an image",
        name="avatar.gif",
        mime="image/gif",
    )

    assert response.status_code == 400
    assert response.get_json()["errors"]["file"] == "Use a JPEG or PNG image."


def test_upload_rejects_mismatched_image_content(client):
    patient = create_patient(client)

    response = upload_photo(
        client,
        patient["id"],
        content=b"not really a PNG",
    )

    assert response.status_code == 400
    assert response.get_json()["errors"]["file"] == (
        "File content does not match the selected image type."
    )


def test_upload_rejects_photo_over_configured_size(client):
    patient = create_patient(client)
    oversized_png = b"\x89PNG\r\n\x1a\n" + (b"x" * (512 * 1024))

    response = upload_photo(client, patient["id"], content=oversized_png)

    assert response.status_code == 400
    assert response.get_json()["errors"]["file"] == (
        "Image size must not exceed 0.5 MB."
    )


def test_upload_rejects_invalid_patient(client):
    response = upload_photo(client, 999)

    assert response.status_code == 404
    assert response.get_json()["message"] == "Patient not found"


def test_upload_sets_verified_false_after_replacement(client):
    patient = create_patient(client)
    upload_photo(client, patient["id"])
    client.patch(
        f"/api/patients/{patient['id']}/photo/verify",
        json={"verified": True},
    )

    response = upload_photo(
        client,
        patient["id"],
        content=JPEG_BYTES,
        name="replacement.jpg",
        mime="image/jpeg",
    )

    assert response.get_json()["data"]["photo_verified"] is False


def test_verify_and_unverify_patient_photo(client):
    patient = create_patient(client)
    upload_photo(client, patient["id"])

    verified = client.patch(
        f"/api/patients/{patient['id']}/photo/verify",
        json={"verified": True},
    )
    unverified = client.patch(
        f"/api/patients/{patient['id']}/photo/verify",
        json={"verified": False},
    )

    assert verified.status_code == 200
    assert verified.get_json()["data"]["photo_verified"] is True
    assert unverified.get_json()["data"]["photo_verified"] is False


def test_verify_patient_photo_requires_boolean(client):
    patient = create_patient(client)
    upload_photo(client, patient["id"])

    response = client.patch(
        f"/api/patients/{patient['id']}/photo/verify",
        json={"verified": "yes"},
    )

    assert response.status_code == 400
    assert response.get_json()["errors"]["verified"] == (
        "A boolean value is required."
    )


def test_delete_patient_photo_clears_metadata_and_object(
    client,
    patient_photo_storage,
):
    patient = create_patient(client)
    upload_photo(client, patient["id"])

    response = client.delete(f"/api/patients/{patient['id']}/photo")
    data = response.get_json()["data"]

    assert response.status_code == 200
    assert data["has_photo"] is False
    assert data["photo_verified"] is False
    assert data["photo_file_name"] is None
    assert data["photo_uploaded_at"] is None
    assert patient_photo_storage.objects == {}
    assert client.get(f"/api/patients/{patient['id']}/photo").status_code == 404
