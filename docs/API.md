# API Documentation

## Base URL
`http://localhost:8000`

## Authentication & Multi-tenancy
All requests require an `X-User-ID` header to identify the user and ensure data isolation.

| Header | Type | Description |
| :--- | :--- | :--- |
| `X-User-ID` | String (UUID recommended) | Unique identifier for the user session/account. |

---

## Endpoints

### 1. Upload Document
Uploads a file for processing and indexing.

- **URL**: `/v1/documents/upload`
- **Method**: `POST`
- **Content-Type**: `multipart/form-data`
- **Headers**: `X-User-ID` (Required)

**Request Body**:
- `file`: The document file (PDF, DOCX, or TXT). Max size: 20MB.

**Response**: `202 Accepted`
```json
{
  "document_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "PROCESSING",
  "filename": "annual_report.pdf"
}
```

### 2. Chat Query
Submit a natural language question based on uploaded documents.

- **URL**: `/v1/chat/query`
- **Method**: `POST`
- **Content-Type**: `application/json`
- **Headers**: `X-User-ID` (Required)

**Request Body**:
```json
{
  "query": "What was the total revenue in 2023?",
  "conversation_id": "optional-uuid",
  "filters": {
    "document_ids": ["uuid1", "uuid2"]
  }
}
```

**Response**: `200 OK`
```json
{
  "answer": "The total revenue in 2023 was $50 million.",
  "sources": [
    {
      "document_id": "uuid1",
      "filename": "annual_report.pdf",
      "page": 12
    }
  ]
}
```

---

## Status Codes
- `200 OK`: Request successful.
- `202 Accepted`: Document upload received and processing started.
- `400 Bad Request`: Invalid file format or missing parameters.
- `401 Unauthorized`: Missing `X-User-ID` header.
- `500 Internal Server Error`: Unexpected server error.
