# UI Components

## Core UI Components

### TaskList Component
**Responsibility**: Display all tasks for the authenticated user with filtering and sorting capabilities
- **Props**: tasks (array of task objects), onUpdate, onDelete, onCompleteToggle
- **Functionality**: Renders list of TaskItem components, provides filtering controls, handles loading states
- **Data Flow**: Receives tasks from parent component, emits update/delete events
- **Styling**: Responsive grid/list layout, consistent with application theme

### TaskItem Component
**Responsibility**: Display individual task with title, description, completion status, and action buttons
- **Props**: task (single task object), onEdit, onDelete, onCompleteToggle
- **Functionality**: Shows task details, completion checkbox, edit/delete buttons, status indicators
- **Data Flow**: Receives task data from parent, emits action events
- **Styling**: Card-based design with clear visual distinction for completed tasks

### AuthForm Component
**Responsibility**: Handle user authentication flows (login/register)
- **Props**: mode ('login' or 'register'), onSubmit, onError
- **Functionality**: Form validation, submission handling, error display, mode switching
- **Data Flow**: Collects user input, submits to authentication service, handles response
- **Styling**: Consistent form layout with proper spacing and validation feedback

### TaskForm Component
**Responsibility**: Allow users to create or update tasks
- **Props**: initialData (optional), onSubmit, onCancel
- **Functionality**: Form fields for title/description, validation, submission handling
- **Data Flow**: Collects task data, validates input, submits to task service
- **Styling**: Modal or inline form with proper input styling and validation feedback

### ProtectedRoute Component
**Responsibility**: Ensure only authenticated users can access certain pages
- **Props**: children, redirectPath
- **Functionality**: Checks authentication status, redirects unauthenticated users
- **Data Flow**: Verifies auth state, conditionally renders children or redirects
- **Styling**: No specific styling, acts as wrapper component

### Navbar Component
**Responsibility**: Provide navigation between application sections and user management
- **Props**: user, onLogout
- **Functionality**: Display navigation links, user profile dropdown, logout functionality
- **Data Flow**: Receives user data, emits logout event
- **Styling**: Fixed header with responsive design

### LoadingSpinner Component
**Responsibility**: Indicate loading states during API requests
- **Props**: isVisible, message
- **Functionality**: Show/hide spinner with optional message
- **Data Flow**: Controlled by parent component via props
- **Styling**: Centered overlay with animation

## Component Responsibilities and Data Flow

### Data Flow Hierarchy
1. **App Component**: Manages global state and authentication
2. **Page Components**: Handle route-specific logic and data fetching
3. **Container Components**: Manage business logic and service interactions
4. **Presentation Components**: Display data and emit user actions

### State Management
- **Authentication State**: Managed at App level, passed down via context or props
- **Tasks State**: Managed at page/container level, updated via service calls
- **UI State**: Local to individual components (form inputs, modal visibility, etc.)

### Event Propagation
- **User Actions**: Emitted from presentation components to container components
- **Service Calls**: Initiated in container components and propagated to services
- **State Updates**: Handled through established state management patterns