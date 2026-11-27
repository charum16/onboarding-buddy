# Onboarding Buddy API

The API is served on port `8080` by default.

- Interactive OpenAPI documentation: `http://localhost:8080/docs`
- OpenAPI schema: `http://localhost:8080/openapi.json`

Unless noted otherwise, request and response bodies use JSON. IDs in paths are
integers.

## Conversations

### Create a conversation

`POST /conversations`

Request:

```json
{
  "convo_name": "New employee onboarding"
}
```

Success response (`201 Created`):

```json
{
  "id": 12,
  "convo_name": "New employee onboarding"
}
```

### List conversations

`GET /conversations`

Success response (`200 OK`):

```json
[
  {
    "id": 12,
    "convo_name": "New employee onboarding"
  }
]
```

### Get a conversation

`GET /conversations/{conversation_id}`

Success response (`200 OK`) has the same shape as one item from the list.
If the conversation does not exist, the API returns `404 Not Found`:

```json
{
  "detail": "Conversation not found"
}
```

### Delete a conversation

`DELETE /conversations/{conversation_id}`

Success response: `204 No Content` (empty body). A missing conversation returns
`404 Not Found`.

## Messages

Messages belong to a conversation. Replace `{convo_id}` with its integer ID.

### List messages

`GET /conversations/{convo_id}/messages`

Success response (`200 OK`):

```json
[
  {
    "id": 34,
    "convo_id": 12,
    "content": "Welcome to the team."
  }
]
```

An empty conversation returns an empty array.

### Ask a question

`POST /conversations/{convo_id}/messages`

Request:

```json
{
  "content": "What should I do on my first day?"
}
```

The retrieval pipeline uses up to 10 previous messages and retrieves up to 3
relevant document chunks. The generated response is saved to the conversation.

Success response (`200 OK`):

```json
{
  "response": "Start by meeting your manager and completing the required setup. [employee-guide.pdf, 2]",
  "chunks": [
    {
      "doc_name": "employee-guide.pdf",
      "page_number": 2,
      "content": "On your first day, meet your manager and complete the required setup."
    }
  ]
}
```

`chunks` contains the retrieved source passages; it may be empty when no chunks
are found.

## Documents

### Upload a document

`POST /documents`

Send a `multipart/form-data` request with:

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `file` | File | Yes | A `.pdf`, `.txt`, or `.md` document. |
| `strategy` | Query parameter | No | Chunking strategy: `fixed_size` (default) or `paragraph`. |

Example:

```bash
curl -X POST 'http://localhost:8080/documents?strategy=fixed_size' \
  -F 'file=@./employee-guide.pdf'
```

Success response (`201 Created`):

```json
{
  "document_id": 7,
  "filename": "employee-guide.pdf",
  "strategy": "fixed_size"
}
```

Unsupported file types, invalid strategies, and documents with no extractable
text return `400 Bad Request`, with a `detail` message describing the problem.