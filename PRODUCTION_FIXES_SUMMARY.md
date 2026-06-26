# Production Fixes Summary for Railway Deployment

## Problem
Frontend was sending requests to itself (frontend domain) using relative URLs like `/api/profile`, causing `405 Method Not Allowed` because the frontend service doesn't handle API routes.

## Solution
Centralized API client with configurable base URL.

---

## Files Created

### 1. `frontend/src/api.js`
- Centralized axios client
- Base URL from `import.meta.env.VITE_API_URL`
- All frontend code imports from this file

### 2. `frontend/.env.example`
- Documents required environment variable
- `VITE_API_URL=https://easygoing-consideration-production-e03e.up.railway.app`

---

## Files Modified

### 3. `frontend/src/App.jsx`
- Changed: `import axios from 'axios'` → `import api from './api'`
- Changed: `axios.get('/api/profiles')` → `api.get('/api/profiles')`

### 4. `frontend/src/components/ProfileBuilder.jsx`
- Changed: `import axios from 'axios'` → `import api from '../api'`
- Changed: `axios.post('/api/profile', ...)` → `api.post('/api/profile', ...)`

### 5. `frontend/src/components/ResumeGenerator.jsx`
- Changed: `import axios from 'axios'` → `import api from '../api'`
- Changed: `axios.post(...)` → `api.post(...)`
- **Critical fix**: Resume download URL changed from `window.location.origin` to `import.meta.env.VITE_API_URL`
  - Previously downloaded from frontend domain (broken)
  - Now downloads from backend Railway service

### 6. `frontend/src/components/JobMatcher.jsx`
- Changed: `import axios from 'axios'` → `import api from '../api'`
- Changed: `axios.get(...)` → `api.get(...)`
- Added array safety guards

---

## Array Safety Guards Added (Previous Session)

To prevent `e.map is not a function` crashes:

### `App.jsx`
```javascript
setProfiles(Array.isArray(response.data) ? response.data : [])
```

### `JobMatcher.jsx`
```javascript
(Array.isArray(profiles) ? profiles : []).slice(0,5).map(...)
(Array.isArray(job.missing_skills) ? job.missing_skills : []).map(...)
if (!Array.isArray(profiles) || profiles.length === 0) { ... }
```

### `ResumeGenerator.jsx`
```javascript
(Array.isArray(profiles) ? profiles : []).map(...)
```

---

## Bug Explanation

**Why did `e.map is not a function` happen?**
- On Railway, when backend returned an error response (e.g., 500, 404, CORS error), the response data was an object like `{detail: "..."}`, not an array
- Frontend called `.map()` on this object, causing the crash
- Fix: Added `Array.isArray()` checks before all array operations

**Why 405 Method Not Allowed?**
- Frontend sent `POST /api/profile` to `https://skillsetu-production-d7b3.up.railway.app/api/profile`
- The frontend service (Nginx/Vite) doesn't handle `/api/*` routes
- Need to send to backend: `https://easygoing-consideration-production-e03e.up.railway.app/api/profile`
- Fix: Centralized API client with `baseURL: import.meta.env.VITE_API_URL`

---

## Deployment Steps

1. Push these changes to GitHub
2. Railway auto-deploys
3. Set environment variable in Railway:
   - `VITE_API_URL=https://easygoing-consideration-production-e03e.up.railway.app`
4. Redeploy frontend

---

## API Endpoints Verified

| Method | Endpoint | File |
|--------|----------|------|
| GET | `/api/profiles` | App.jsx |
| POST | `/api/profile` | ProfileBuilder.jsx |
| POST | `/api/resume/:id` | ResumeGenerator.jsx |
| GET | `/api/profile/:id/matches` | JobMatcher.jsx |

No `localhost`, `127.0.0.1`, or hardcoded URLs remain in frontend code.

---

## Remaining Issues
- None identified
- Ready for Railway redeployment