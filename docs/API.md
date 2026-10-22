# REST API

All paths are under `/api`. Requests/responses use JSON. Authentication uses `di_session`; no bearer token or frontend-supplied owner is supported. Content endpoints also require authentication because this is a private archive.

| Method | Path               | Request                             | Success                              |
| ------ | ------------------ | ----------------------------------- | ------------------------------------ |
| GET    | `/health`          | None                                | 200 after DB query                   |
| POST   | `/auth/register`   | `{email,password}`                  | 201 user; does not implicitly log in |
| POST   | `/auth/login`      | `{email,password}`                  | 200 user plus session cookie         |
| POST   | `/auth/logout`     | None                                | 204; revokes current session         |
| GET    | `/auth/me`         | Cookie                              | 200 `{id,email}`                     |
| GET    | `/species`         | Cookie                              | 200 content array                    |
| GET    | `/classes`         | Cookie                              | 200 content array                    |
| GET    | `/weapons`         | Cookie                              | 200 weapon array                     |
| GET    | `/characters`      | Cookie                              | 200 owned sheet array                |
| POST   | `/characters`      | `{name,speciesId,classId,weaponId}` | 201 sheet and Location header        |
| GET    | `/characters/{id}` | Cookie                              | 200 owned sheet                      |
| PATCH  | `/characters/{id}` | `{name}`                            | 200 renamed owned sheet              |
| DELETE | `/characters/{id}` | Cookie                              | 204                                  |

All mutations must send the exact configured `Origin`, including CLI/integration clients. Browser fetch sends it automatically. POST/PATCH JSON bodies use `Content-Type: application/json`. Unknown fields are rejected. Name is trimmed, limited to 80 characters and cannot contain control characters. Emails are trimmed/lowercased; passwords are never trimmed.

Errors:

```json
{ "error": { "code": "NOT_FOUND", "message": "Character not found." } }
```

Status categories: 400 invalid fields/IDs/content/JSON, 401 authentication required or incorrect credentials, 403 origin rejected, 404 missing or unowned character, 409 email unavailable, 413 request too large, 429 authentication attempts exceeded, 500 unexpected API/database error, 503 frontend cannot reach the API. Responses containing account/character data are not cacheable. Detailed server errors stay in server logs.

Character responses contain `id`, `name`, `species`, `characterClass`, `level`, `attributes`, `currentWounds`, `calculated` (`movement`, `maxWounds`) and `equipment`. Weapon entries include description, category, damage dice/type, normal/long ranges and structured properties. UUIDs are opaque identifiers, not authorization credentials.
