# Patient Photos

Patient photos provide a visual identity aid while preserving a reliable
initials fallback.

## Display Behavior

- An uploaded photo is shown when available.
- Without a photo, SeniorMate uses the patient's initials.
- A generic avatar appears if the name is unavailable.
- Broken private-storage links fall back instead of showing a broken image.

## Upload or Replace

From Patient Detail, authorized users can upload JPEG or PNG files. The default
limit is 5 MB. Replacing a photo removes the prior object where possible and
sets verification status to unverified.

## Verification

Administrators and managers can mark a photo verified or unverified. This is a
simple status marker; role-specific approval workflows may be added later.

## Delete

Photo deletion requires confirmation. It removes the MinIO object where
possible, clears patient photo metadata, and restores the initials fallback.
