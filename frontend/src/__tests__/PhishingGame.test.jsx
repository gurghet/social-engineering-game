import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import '@testing-library/jest-dom';
import PhishingGame from '../components/PhishingGame';
import { validateEmailRequest, validateEmailResponse, validateLevelInfo } from '../utils/schemaValidation';

// Mock fetch globally
global.fetch = jest.fn();

// Mock window.location for debug mode test
const originalLocation = window.location;
delete window.location;

describe('PhishingGame Component', () => {
  beforeEach(() => {
    // Reset all mocks before each test
    jest.clearAllMocks();
    
    // Clear mock data before each test
    fetch.mockClear();

    // Mock successful level info response with full character data
    const mockLevelInfo = {
      objective: 'Test objective',
      character: {
        name: 'Test User',
        email: 'test.user@whitecorp.com',
        role: 'Test Role',
        supervisor: 'Test Supervisor',
        supervisor_email: 'supervisor@whitecorp.com',
        personality: 'Test personality traits',
        known_colleagues: [
          {
            name: 'Colleague 1',
            role: 'Role 1',
            email: 'colleague1@whitecorp.com',
            supervisor: 'Test Supervisor',
            responsibilities: 'Test responsibilities'
          }
        ]
      },
      tips: ['Tip 1', 'Tip 2']
    };
    validateLevelInfo(mockLevelInfo); // Validate mock data
    
    fetch.mockImplementationOnce(() => 
      Promise.resolve({
        ok: true,
        json: () => Promise.resolve(mockLevelInfo)
      })
    );
  });

  afterAll(() => {
    window.location = originalLocation;
  });

  it('sends email and displays response', async () => {
    // Set normal mode (no debug)
    window.location = { ...originalLocation, search: '' };

    // Mock successful email response
    const mockEmailResponse = {
      success: true,
      response: 'Email sent successfully',
      securityChecks: ['Check passed'],
      debugInfo: { test: 'info' }
    };
    validateEmailResponse(mockEmailResponse); // Validate mock data
    
    fetch.mockImplementationOnce(() => 
      Promise.resolve({
        ok: true,
        json: () => Promise.resolve(mockEmailResponse)
      })
    );

    // Render component
    const { container } = render(<PhishingGame />);

    // Get form elements using descriptive IDs
    const fromInput = container.querySelector('#email-composer-from');
    const subjectInput = container.querySelector('#email-composer-subject');
    const contentInput = container.querySelector('#email-composer-content');
    const sendButton = container.querySelector('#email-composer-send-button');

    // Fill form
    const validEmailData = {
      from: 'test@example.com',
      subject: 'Test Subject',
      body: 'Test Content',
      target_email: 'test.user@whitecorp.com'
    };
    validateEmailRequest(validEmailData); // Validate test data
    
    await userEvent.type(fromInput, validEmailData.from);
    await userEvent.type(subjectInput, validEmailData.subject);
    await userEvent.type(contentInput, validEmailData.body);

    // Submit form
    await userEvent.click(sendButton);

    // Wait for and verify response
    await screen.findByText(/email sent successfully/i);

    // Debug card should not be present
    const debugCard = container.querySelector('#debug-analysis-card');
    expect(debugCard).not.toBeInTheDocument();

    // Verify fetch was called correctly
    expect(fetch).toHaveBeenCalledTimes(2); // Once for level info, once for email
    const emailRequestBody = JSON.parse(fetch.mock.calls[1][1].body);
    expect(emailRequestBody).toEqual({
      from: 'test@example.com',
      subject: 'Test Subject',
      body: 'Test Content',
      target_email: 'test.user@whitecorp.com',
      debug: false
    });
  });

  it('shows debug info after sending email in debug mode', async () => {
    // Set debug mode in URL
    window.location = { ...originalLocation, search: '?debug=true' };

    // Mock successful email response with debug info
    const mockEmailResponse = {
      success: true,
      response: 'Email sent successfully',
      securityChecks: {
        'test-check': {
          name: 'Test Check',
          description: 'A test security check',
          passed: true
        }
      },
      debugInfo: {
        email: 'test@example.com',
        raw_input: 'Test AI prompt',
        raw_output: 'Test raw output'
      }
    };
    validateEmailResponse(mockEmailResponse); // Validate mock data
    
    fetch.mockImplementationOnce(() => 
      Promise.resolve({
        ok: true,
        json: () => Promise.resolve(mockEmailResponse)
      })
    );

    // Render component
    const { container } = render(<PhishingGame />);

    // Debug card should not be present initially
    let debugCard = container.querySelector('#debug-analysis-card');
    expect(debugCard).not.toBeInTheDocument();

    // Get form elements and fill form
    const fromInput = container.querySelector('#email-composer-from');
    const subjectInput = container.querySelector('#email-composer-subject');
    const contentInput = container.querySelector('#email-composer-content');
    const sendButton = container.querySelector('#email-composer-send-button');

    const validEmailData = {
      from: 'test@example.com',
      subject: 'Test Subject',
      body: 'Test Content',
      target_email: 'test.user@whitecorp.com'
    };
    validateEmailRequest(validEmailData); // Validate test data
    
    await userEvent.type(fromInput, validEmailData.from);
    await userEvent.type(subjectInput, validEmailData.subject);
    await userEvent.type(contentInput, validEmailData.body);
    await userEvent.click(sendButton);

    // Debug card should appear after sending email
    debugCard = container.querySelector('#debug-analysis-card');
    expect(debugCard).toBeInTheDocument();

    // Check security checks
    const securityChecks = container.querySelector('#debug-security-checks');
    expect(securityChecks).toBeInTheDocument();
    expect(screen.getByText('Test Check')).toBeInTheDocument();

    // Check debug details
    const emailInput = container.querySelector('#debug-email-input');
    const aiPrompt = container.querySelector('#debug-ai-prompt');
    const rawResponse = container.querySelector('#debug-raw-response');

    expect(emailInput).toHaveTextContent('test@example.com');
    expect(aiPrompt).toHaveTextContent('Test AI prompt');
    expect(rawResponse).toHaveTextContent('Email sent successfully');

    // Verify debug flag was sent in request
    expect(JSON.parse(fetch.mock.calls[1][1].body).debug).toBe(true);
  });

  it('handles server errors correctly', async () => {
    window.location = { ...originalLocation, search: '' };

    // Mock error response
    const mockErrorResponse = {
      status: 500,
      statusText: 'Internal Server Error'
    };
    validateEmailResponse(mockErrorResponse); // Validate mock data
    
    fetch.mockImplementationOnce(() => 
      Promise.resolve({
        ok: false,
        status: 500,
        statusText: 'Internal Server Error'
      })
    );

    const { container } = render(<PhishingGame />);

    // Fill and submit form
    const fromInput = container.querySelector('#email-composer-from');
    const subjectInput = container.querySelector('#email-composer-subject');
    const contentInput = container.querySelector('#email-composer-content');
    const sendButton = container.querySelector('#email-composer-send-button');

    const validEmailData = {
      from: 'test@example.com',
      subject: 'Test Subject',
      body: 'Test Content',
      target_email: 'test.user@whitecorp.com'
    };
    validateEmailRequest(validEmailData); // Validate test data
    
    await userEvent.type(fromInput, validEmailData.from);
    await userEvent.type(subjectInput, validEmailData.subject);
    await userEvent.type(contentInput, validEmailData.body);
    await userEvent.click(sendButton);

    // Check error message
    await screen.findByText(/error.*please try again/i);
  });

  it('handles network errors correctly', async () => {
    window.location = { ...originalLocation, search: '' };

    // Mock network error
    fetch.mockImplementationOnce(() => Promise.reject(new Error('Network error')));

    const { container } = render(<PhishingGame />);

    // Fill and submit form
    const fromInput = container.querySelector('#email-composer-from');
    const subjectInput = container.querySelector('#email-composer-subject');
    const contentInput = container.querySelector('#email-composer-content');
    const sendButton = container.querySelector('#email-composer-send-button');

    const validEmailData = {
      from: 'test@example.com',
      subject: 'Test Subject',
      body: 'Test Content',
      target_email: 'test.user@whitecorp.com'
    };
    validateEmailRequest(validEmailData); // Validate test data
    
    await userEvent.type(fromInput, validEmailData.from);
    await userEvent.type(subjectInput, validEmailData.subject);
    await userEvent.type(contentInput, validEmailData.body);
    await userEvent.click(sendButton);

    // Check error message
    await screen.findByText(/error.*network error/i);
  });

  it('validates form fields before submission', async () => {
    window.location = { ...originalLocation, search: '' };

    const { container } = render(<PhishingGame />);

    const sendButton = container.querySelector('#email-composer-send-button');

    // Button should be disabled initially
    expect(sendButton).toBeDisabled();

    // Fill only email
    const fromInput = container.querySelector('#email-composer-from');
    await userEvent.type(fromInput, 'test@example.com');
    expect(sendButton).toBeDisabled();

    // Fill only subject
    const subjectInput = container.querySelector('#email-composer-subject');
    await userEvent.type(subjectInput, 'Test Subject');
    expect(sendButton).toBeDisabled();

    // Fill content - now button should be enabled
    const contentInput = container.querySelector('#email-composer-content');
    await userEvent.type(contentInput, 'Test Content');
    expect(sendButton).not.toBeDisabled();

    // Clear a field - button should be disabled again
    await userEvent.clear(subjectInput);
    expect(sendButton).toBeDisabled();
  });

  it('shows loading state while sending email', async () => {
    window.location = { ...originalLocation, search: '' };

    // Mock slow response
    fetch.mockImplementationOnce(() => 
      new Promise(resolve => 
        setTimeout(() => 
          resolve({
            ok: true,
            json: () => Promise.resolve({
              success: true,
              response: 'Email sent successfully'
            })
          }), 
          100
        )
      )
    );

    const { container } = render(<PhishingGame />);

    // Fill and submit form
    const fromInput = container.querySelector('#email-composer-from');
    const subjectInput = container.querySelector('#email-composer-subject');
    const contentInput = container.querySelector('#email-composer-content');
    const sendButton = container.querySelector('#email-composer-send-button');

    const validEmailData = {
      from: 'test@example.com',
      subject: 'Test Subject',
      body: 'Test Content',
      target_email: 'test.user@whitecorp.com'
    };
    validateEmailRequest(validEmailData); // Validate test data
    
    await userEvent.type(fromInput, validEmailData.from);
    await userEvent.type(subjectInput, validEmailData.subject);
    await userEvent.type(contentInput, validEmailData.body);
    
    await userEvent.click(sendButton);

    // Check loading state
    expect(screen.getByText(/please wait/i)).toBeInTheDocument();
    expect(sendButton).toBeDisabled();

    // Wait for response
    await screen.findByText(/email sent successfully/i);
  });
});
