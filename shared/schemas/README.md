# Shared JSON Schemas

This directory contains JSON schemas that are shared between the frontend and backend.

## Schemas

### Email Schema (`email.json`)
- `email_request`: Schema for email requests sent to the backend
- `email_response`: Schema for responses from the email endpoint

### Level Schema (`level.json`)
- `level_info`: Schema for individual level information
- `levels_response`: Schema for the list of available levels

## Usage

### Backend (Python)
```python
import json
from jsonschema import validate, FormatChecker

# Load schemas
with open('shared/schemas/email.json') as f:
    email_schemas = json.load(f)

# Validate request
validate(
    instance=request_data,
    schema=email_schemas['email_request'],
    format_checker=FormatChecker()
)
```

### Frontend (JavaScript)
```javascript
import emailSchemas from '../../shared/schemas/email.json';
import Ajv from 'ajv';
import addFormats from 'ajv-formats';

const ajv = new Ajv();
addFormats(ajv);

// Create validators
const validateEmailRequest = ajv.compile(emailSchemas.email_request);
const validateEmailResponse = ajv.compile(emailSchemas.email_response);

// Validate data
const isValid = validateEmailRequest(data);
if (!isValid) console.error(validateEmailRequest.errors);
```

### E2E Tests (TypeScript)
```typescript
import { test, expect } from '@playwright/test';
import emailSchemas from '../../shared/schemas/email.json';
import Ajv from 'ajv';
import addFormats from 'ajv-formats';

const ajv = new Ajv();
addFormats(ajv);

test('email response should match schema', async ({ request }) => {
  const response = await request.post('/api/send_email', {
    data: {
      from: 'test@example.com',
      subject: 'Test',
      body: 'Test content'
    }
  });
  
  const data = await response.json();
  const validate = ajv.compile(emailSchemas.email_response);
  expect(validate(data)).toBe(true);
});
```
