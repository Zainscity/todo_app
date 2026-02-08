# Page Structure

## App Router Page Structure

### Public Pages
- **/ (Home)**: Landing page with application overview and call-to-action for registration
  - **Components**: Hero section, feature highlights, login/register links
  - **Authentication**: No authentication required
  - **Navigation**: Links to login/register, footer with additional information

- **/login**: User authentication page
  - **Components**: AuthForm (login mode), "Don't have an account?" link
  - **Authentication**: No authentication required
  - **Navigation**: Link to registration page, home page link

- **/register**: User registration page
  - **Components**: AuthForm (register mode), "Already have an account?" link
  - **Authentication**: No authentication required
  - **Navigation**: Link to login page, home page link

### Protected Pages
- **/dashboard** (Default redirect after login): User's task management center
  - **Components**: Navbar, TaskList, TaskForm (collapsed by default)
  - **Authentication**: Required authentication
  - **Navigation**: Accessible only when authenticated, logout option in navbar

- **/tasks**: Dedicated task management page
  - **Components**: Navbar, TaskList, TaskForm (expanded by default)
  - **Authentication**: Required authentication
  - **Navigation**: Accessible only when authenticated, links to other protected pages

- **/profile**: User profile and account management
  - **Components**: Navbar, UserProfileForm, SecuritySettings
  - **Authentication**: Required authentication
  - **Navigation**: Accessible only when authenticated, typically accessed via navbar dropdown

## Protected vs Public Pages

### Public Pages Characteristics
- **Access**: Available to all users regardless of authentication status
- **Content**: Marketing, informational, or authentication-related content
- **Layout**: May use simplified layout without navigation bar
- **Data**: Static content or anonymous API calls only
- **Routing**: Direct access allowed, no redirect to login required

### Protected Pages Characteristics
- **Access**: Available only to authenticated users
- **Content**: Personalized user data and functionality
- **Layout**: Full layout with navigation bar and user context
- **Data**: Requires authentication tokens for API access
- **Routing**: Unauthenticated access redirects to login page

## Navigation Flow After Login/Logout

### Login Flow
1. **User Action**: Successfully logs in on /login or /register page
2. **Redirect**: Automatically redirected to /dashboard (or last visited protected page)
3. **State Update**: Authentication state updated in application context
4. **UI Update**: Navbar shows user profile, public links replaced with protected navigation
5. **Data Fetch**: Protected data begins loading based on user context

### Logout Flow
1. **User Action**: Clicks logout in navbar dropdown or on profile page
2. **Token Cleanup**: JWT token cleared from storage, session invalidated
3. **State Reset**: Authentication state cleared in application context
4. **Redirect**: Navigated to home page (/) or login page (/login)
5. **UI Update**: Navbar switches to public state, protected content hidden
6. **Data Clearance**: Personal data cleared from client-side state

### Navigation Guards
- **Route Protection**: Middleware ensures protected routes require authentication
- **Automatic Redirects**: Unauthenticated users redirected to login when accessing protected content
- **Preserved Intent**: Remember user's intended destination for post-login redirect
- **Session Monitoring**: Continuous session validity checks with automatic logout on token expiration