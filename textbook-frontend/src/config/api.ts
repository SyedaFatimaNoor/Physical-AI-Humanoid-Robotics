// src/config/api.ts
const API_BASE_URL = process.env.REACT_APP_API_URL || '';

export const getApiUrl = (endpoint: string): string => {
    // If API_BASE_URL is set, use it; otherwise use relative path
    return API_BASE_URL ? `${API_BASE_URL}${endpoint}` : endpoint;
};

export default {
    chat: getApiUrl('/api/chat'),
    translate: getApiUrl('/api/translate'),
    personalize: getApiUrl('/api/personalize'),
    signup: getApiUrl('/api/signup'),
    signin: getApiUrl('/api/signin'),
};
