# Secure File Sharing System

A secure file-sharing API allowing Operations users to upload files and Client users to download them through encrypted URLs.

## Features

- **User Authentication**: Separate roles for Operations and Client users
- **File Upload**: Operations users can upload PPTX, DOCX, and XLSX files
- **Secure Downloads**: Client users receive encrypted download URLs
- **Email Verification**: Client users must verify their email before accessing the system
- **Authorization**: Role-based access controls for all operations

## API Endpoints

### Authentication

- `POST /api/auth/register` - Register a new client user
- `POST /api/auth/create-ops` - Create an operations user
- `GET /api/auth/verify/:token` - Verify email address
- `POST /api/auth/login` - Login (both user types)
- `GET /api/auth/profile` - Get current user profile

### File Management

- `POST /api/files/upload` - Upload a file (operations users only)
- `GET /api/files` - List all files (client users only)
- `GET /api/files/download/:id` - Generate download link (client users only)
- `GET /api/files/download-file/:token` - Download file with encrypted token (client users only)
- `DELETE /api/files/:id` - Delete a file (operations users only)

## Setup

1. Clone the repository
2. Install dependencies:
   ```
   npm install
   ```
3. Create a `.env` file with the necessary environment variables (see `.env.example`)
4. Start the server:
   ```
   npm run dev
   ```

## Deployment Plan

For deploying this application to production:

1. **Environment Setup**:
   - Dedicated MongoDB Atlas cluster for production
   - Secure storage for file uploads (AWS S3 or similar)
   - Environment variables management through CI/CD pipeline

2. **Security Measures**:
   - HTTPS implementation
   - API rate limiting
   - IP whitelisting for admin operations
   - Regular security audits

3. **Deployment Steps**:
   - Set up CI/CD pipeline (GitHub Actions, Jenkins, etc.)
   - Create staging environment for testing
   - Automate testing with the included Postman tests
   - Deploy to production server (AWS, Azure, GCP, etc.)
   - Set up monitoring and logging (CloudWatch, ELK stack, etc.)

4. **Scalability**:
   - Implement horizontal scaling for the API service
   - Use a load balancer for traffic distribution
   - Set up database sharding for larger deployments

## Postman Tests

A comprehensive Postman collection is included in the repository to test all API endpoints. Import `postman_tests.json` into Postman to run the tests.