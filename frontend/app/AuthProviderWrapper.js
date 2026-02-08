'use client';

import { AuthProvider } from '../src/context/AuthContext';

export default function AuthProviderWrapper({ children }) {
  return (
    <AuthProvider>
      {children}
    </AuthProvider>
  );
}