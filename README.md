# 🚀 MCP Server UI - Memory Context Manager v2

A beautiful, modern web interface for the **Memory Context Manager v2** MCP server, built with **RedwoodJS** and **Chakra UI**. This UI showcases our **Continuous Self-Evolution System** and provides real-time monitoring of our autonomous AI capabilities.

## ✨ Features

### 🎯 **Dashboard Overview**

- **Real-time System Health** monitoring with beautiful progress bars
- **Evolution Engine Status** showing continuous self-improvement
- **MCP Server Metrics** with connection and tool availability
- **Recent Activity Feed** tracking all system operations
- **Quick Actions** for immediate system control

### 🧠 **Evolution Engine Interface**

- **Comprehensive Evolution Metrics** with detailed breakdowns
- **Scheduled Tasks Management** with priority and timing
- **Recent Evolutions History** showing learning progress
- **Learning Sources Tracking** from documentation ingestion
- **System Health Monitoring** with background processes

### 🎨 **Modern UI/UX**

- **Chakra UI Components** for consistent, accessible design
- **Responsive Layout** that works on all devices
- **Custom Theme** with brand colors and evolution accents
- **Interactive Elements** with hover effects and animations
- **Professional Dashboard** layout with sidebar navigation

## 🏗️ Architecture

### **Frontend Stack**

- **RedwoodJS** - Full-stack React framework
- **Chakra UI** - Modern component library
- **TypeScript** - Type-safe development
- **React Icons** - Beautiful iconography

### **Backend Integration**

- **MCP Server** - Memory Context Manager v2
- **Evolution Engine** - Continuous self-improvement
- **Real-time Data** - Live system monitoring
- **API Endpoints** - RESTful communication

## 🚀 Getting Started

### **Prerequisites**

- Node.js 18+
- Yarn package manager
- MCP Server running (Memory Context Manager v2)

### **Installation**

1. **Clone the repository**

   ```bash
   git clone <repository-url>
   cd mcp-server-ui
   ```

2. **Install dependencies**

   ```bash
   yarn install
   ```

3. **Start the development server**

   ```bash
   yarn rw dev
   ```

4. **Open your browser**
   Navigate to `http://localhost:8910`

## 📱 Pages & Features

### **🏠 Dashboard Page (`/`)**

- **System Health Overview**: Real-time metrics with progress bars
- **Evolution Engine Status**: Current evolution progress and statistics
- **MCP Server Status**: Connection status and tool availability
- **Recent Activity**: Timeline of system operations
- **Quick Actions**: Immediate system control buttons

### **⚡ Evolution Engine Page (`/evolution-engine`)**

- **Evolution Metrics**: Detailed breakdown of system improvements
- **Scheduled Tasks**: Management of upcoming evolution tasks
- **Recent Evolutions**: History of completed improvements
- **Learning Sources**: Documentation sources and learning progress
- **System Health**: Background processes and resource usage

## 🎨 Design System

### **Color Palette**

- **Brand Colors**: Professional blue tones for primary elements
- **Evolution Colors**: Purple accents for evolution-related features
- **Status Colors**: Green (success), Yellow (warning), Red (error)
- **Neutral Colors**: Gray scale for text and borders

### **Component Library**

- **Cards**: Clean, elevated containers for content
- **Progress Bars**: Visual representation of metrics
- **Badges**: Status indicators and labels
- **Tables**: Organized data presentation
- **Tabs**: Organized content sections
- **Alerts**: Important information notifications

## 🔧 Configuration

### **Environment Variables**

```bash
# MCP Server Configuration
MCP_SERVER_URL=http://localhost:8000
MCP_SERVER_TIMEOUT=30000

# Evolution Engine Settings
EVOLUTION_CHECK_INTERVAL=5000
EVOLUTION_MAX_CONCURRENT=3
```

### **Theme Customization**

The Chakra UI theme can be customized in `web/src/App.tsx`:

```typescript
const theme = extendTheme({
  colors: {
    brand: {
      /* Custom brand colors */
    },
    evolution: {
      /* Custom evolution colors */
    },
  },
  components: {
    Button: {
      /* Custom button styles */
    },
  },
})
```

## 📊 Data Integration

### **MCP Server Communication**

- **Real-time Updates**: Live data from evolution engine
- **Status Monitoring**: Server health and connection status
- **Tool Management**: Available MCP tools and their status
- **Performance Metrics**: System performance indicators

### **Evolution Engine Data**

- **Learning Progress**: Documentation ingestion status
- **Evolution Metrics**: Performance improvements over time
- **Task Scheduling**: Upcoming evolution tasks
- **System Health**: Resource usage and background processes

## 🚀 Deployment

### **Production Build**

```bash
# Build the application
yarn rw build

# Start production server
yarn rw serve
```

### **Docker Deployment**

```bash
# Build Docker image
docker build -t mcp-server-ui .

# Run container
docker run -p 8910:8910 mcp-server-ui
```

## 🔍 Monitoring & Analytics

### **System Metrics**

- **Overall Health Score**: Composite system performance
- **Performance Metrics**: Speed and efficiency indicators
- **Intelligence Score**: AI capability measurements
- **Adaptability Rating**: System flexibility and learning

### **Evolution Tracking**

- **Success Rate**: Percentage of successful evolutions
- **Learning Sources**: Documentation sources and impact
- **Improvement Trends**: Performance over time
- **Resource Usage**: Memory and CPU consumption

## 🧪 Testing

### **Run Tests**

```bash
# Unit tests
yarn rw test

# Integration tests
yarn rw test --watch

# E2E tests
yarn rw test:e2e
```

### **Test Coverage**

```bash
# Generate coverage report
yarn rw test --coverage
```

## 🤝 Contributing

### **Development Workflow**

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

### **Code Standards**

- **TypeScript**: Strict type checking enabled
- **ESLint**: Code quality and consistency
- **Prettier**: Code formatting
- **Chakra UI**: Component library usage

## 📚 Documentation

### **API Reference**

- **MCP Server Tools**: Available MCP server functions
- **Evolution Engine**: Continuous self-improvement API
- **System Health**: Monitoring and metrics endpoints

### **Component Library**

- **Chakra UI Components**: Usage examples and props
- **Custom Components**: Dashboard-specific components
- **Layout System**: Responsive design patterns

## 🌟 Showcase

This UI demonstrates the power of our **Continuous Self-Evolution System**:

- **🎯 Autonomous Learning**: System learns from documentation automatically
- **📈 Performance Improvement**: Real-time metrics showing system evolution
- **🔄 Background Processing**: Continuous optimization without user intervention
- **🧠 Intelligent Adaptation**: System adapts to new knowledge sources
- **📊 Visual Monitoring**: Beautiful dashboards for system oversight

## 🔮 Future Enhancements

### **Planned Features**

- **Real-time WebSocket** updates for live data
- **Advanced Analytics** with charts and graphs
- **User Management** with role-based access
- **API Documentation** with interactive testing
- **Mobile App** for on-the-go monitoring

### **Integration Possibilities**

- **Grafana Dashboards** for advanced metrics
- **Slack Notifications** for system alerts
- **GitHub Integration** for code-based learning
- **CI/CD Pipeline** for automated deployment

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **RedwoodJS Team** for the amazing full-stack framework
- **Chakra UI Team** for the beautiful component library
- **MCP Community** for the Model Context Protocol
- **Open Source Contributors** for inspiration and tools

---

**Built with ❤️ using RedwoodJS + Chakra UI**

**Showcasing the future of autonomous AI systems** 🚀🧠✨
