import Ajv from 'ajv';
import addFormats from 'ajv-formats';
import emailSchemas from '../../../shared/schemas/email.json';
import levelSchemas from '../../../shared/schemas/level.json';

const ajv = new Ajv();
addFormats(ajv);

// Create validators
export const validateEmailRequest = ajv.compile(emailSchemas.email_request);
export const validateEmailResponse = ajv.compile(emailSchemas.email_response);
export const validateLevelInfo = ajv.compile(levelSchemas.level_info);
export const validateLevelsResponse = ajv.compile(levelSchemas.levels_response);

/**
 * Validate data against a schema
 * @param {Object} data - Data to validate
 * @param {Function} validator - Schema validator function
 * @returns {boolean} True if valid, throws error if invalid
 */
export const validateData = (data, validator) => {
  const isValid = validator(data);
  if (!isValid) {
    console.error('Schema validation errors:', validator.errors);
    throw new Error(`Schema validation failed: ${JSON.stringify(validator.errors)}`);
  }
  return true;
};
