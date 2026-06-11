# Medical Records

Medical Records attach private documents to a patient. File bytes are stored
in MinIO, while searchable metadata is stored in PostgreSQL.

## Supported Files

- PDF
- JPEG
- PNG
- DOC
- DOCX

The default file-size limit is 10 MB and can be changed by an administrator.

## Upload

From Patient Detail, open Medical Records and provide:

- Title
- File
- Optional description
- Optional record type
- Optional uploader name

## Download, Edit, and Delete

Authorized users can update metadata or delete a record. Download access uses
the backend and does not expose the private MinIO bucket. Deleting a record
removes its database metadata and attempts to remove the stored object.

Administrators, managers, and nurses can manage records. Caregivers and
viewers can view and download them.
