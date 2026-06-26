# Railway Deployment Fix

## Problem
Frontend on Railway is not sending requests to the backend because the `VITE_API_URL` environment variable is likely not set in the Railway frontend service.

## Fix
In Railway Dashboard:

1. Go to your **frontend** service
2. Click **Variables** tab
3. Add:
   - Key: `VITE_API_URL`
   - Value: `https://easygoing-consideration-production-e03e.up.railway.app`
4. Click **Deploy** or **Redeploy**

## Verify
After redeploy, open the frontend and check browser console:
- Should log API URL
- Requests should go to `easygoing-consideration-production-e03e.up.railway.app`