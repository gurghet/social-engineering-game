import React from 'react';
import { render, screen } from '@testing-library/react';

function SimpleComponent() {
  return <div>Test is working!</div>;
}

describe('Test Setup', () => {
  test('renders without crashing', () => {
    render(<SimpleComponent />);
    expect(screen.getByText('Test is working!')).toBeInTheDocument();
  });
});
