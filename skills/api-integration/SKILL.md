---
name: api-integration
description: >-
  Integrate mobile, web, and desktop frontend applications with backend REST, GraphQL, or RPC APIs.
  Parses request/response contracts, builds type-safe DTO models, implements repositories/services with
  interceptor auth, handles 401 token refresh, pagination, and error states. Use when user invokes /api-integration
  or asks to "integrate API", "connect backend endpoint", "add api service", or "implement network call".
---

# API Integration Workflow

This workflow guides the implementation of robust, type-safe API integrations across Flutter, React, Next.js, and other frontend stacks. It guarantees accurate contract mapping, centralized network management, secure auth header attachment, automatic token refresh, and complete error handling.

> [!IMPORTANT]
> **Strict Anti-Hallucination Policy**: Never invent endpoint URLs, header keys, payload parameters, or response JSON schemas. Always inspect existing backend route definitions, Swagger/OpenAPI schemas, Postman collections, or ask the user for the concrete API contract before writing client code.

---

## 7-Phase Execution Lifecycle

### Phase 1: Contract Discovery & Verification
1. Locate the exact API contract:
   - Backend routes (e.g. `routes/api.php`, Express/NestJS controllers, FastAPI routes).
   - OpenAPI/Swagger JSON or YAML docs.
   - Example network responses provided by the user.
2. Confirm the details:
   - **Method**: `GET`, `POST`, `PUT`, `PATCH`, `DELETE`.
   - **Base URL & Path**: (e.g., `/api/v1/users/:id`).
   - **Authentication**: Bearer Token, API Key, Session Cookie, OAuth2.
   - **Request Headers**: `Content-Type: application/json`, `Accept: application/json`.
   - **Request Body / Query Params**: Exact parameter names and types.
   - **Response Schemas**: 200/201 Success schema, pagination metadata, error payload formats (e.g., 400 validation errors, 401 Unauthorized, 404 Not Found, 500 Server Error).

---

### Phase 2: Inspect Existing Network Architecture
Inspect the current client-side network stack:
- **Flutter**: Dio vs `http`. Locate existing client instances, interceptors, and base options in `lib/core/network/` or `lib/services/`.
- **Next.js / React**: Axios, native `fetch` with Next.js revalidation, TanStack Query / SWR, or RTK Query.
- **Rules**:
  - Reuse the existing HTTP client and base URL configuration.
  - Never instantiate a raw new `http.Client()` or unconfigured `fetch()` that bypasses global authentication or error interceptors!

---

### Phase 3: Type-Safe Data Models (DTOs & Entities)
Create models with robust serialization/deserialization:
- **Flutter / Dart**:
  - Use `fromJson` / `toJson` factory methods.
  - Apply immutability (Freezed / Equatable / Dart 3 Records).
  - Handle nullability safely (fallback defaults for optional fields).
- **TypeScript / React**:
  - Write explicit interfaces and types.
  - Validate payloads at runtime using Zod or Valibot when untrusted inputs are expected.

---

### Phase 4: Service & Repository Layer Implementation
1. **API Service / Data Source**:
   - Implements the raw HTTP call using the project's centralized client.
   - Converts exceptions into typed failure objects (e.g., `ServerFailure`, `NetworkFailure`, `UnauthorizedFailure`).
2. **Repository Layer**:
   - Exposes clean domain methods returning typed Results/Either/Exceptions.
   - Implements caching or local storage persistence if required.
3. **Pagination & File Uploads**:
   - For lists: Support cursor-based or offset/limit pagination.
   - For file uploads: Use `FormData` / `MultipartFile` with proper MIME types.

---

### Phase 5: State Management & UI Binding
Connect the repository to the UI layer:
- **Flutter**: Emit states in Cubit/Bloc/Notifier (`Loading`, `Success(data)`, `Failure(message)`).
- **React / Next.js**: Use TanStack Query `useQuery` / `useMutation` with proper query keys and invalidate tags on mutations.
- **Auth Expiration (401)**: Verify that the network client's auth interceptor intercepts 401s, attempts refresh token exchange, or redirects to login gracefully without crashing.

---

### Phase 6: Automated Testing
1. **Mocking**: Mock HTTP responses with realistic JSON payloads.
2. **Unit Tests**:
   - Test JSON deserialization with valid and missing/null fields.
   - Test successful API response mapping.
   - Test error status handling (400, 401, 500, network timeouts).

---

### Phase 7: Verification & Final Report
1. Run analyzers and unit tests:
   - Flutter: `flutter test test/path/to/api_test.dart`
   - React / Next.js: `npm test`
2. Present integration report:
   - Endpoints connected.
   - Created Models & Repositories.
   - Authentication & Error handling details.
   - Verification status.

---

## Shared References
- [Global Engineering Standards](../../references/global-engineering-standards.md)
