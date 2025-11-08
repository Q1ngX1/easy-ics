# Easy ICS 📅# Easy ICS 📅



> Intelligent tool to convert images and text into standard calendar files[English](README.md) | [中文](README.zh-CN.md)



**[English](README.md) | [中文](README.zh-CN.md)**Intelligent tool to convert images and text into calendar files



---## ✨ Core Features



## Overview- 🖼️ **OCR Image Recognition** - Extract calendar information from images

- 📝 **Text Parsing** - Extract events from natural language text

Easy ICS is a comprehensive full-stack application designed to solve a universal problem: the tedious manual entry of calendar events. Whether you have a scanned paper schedule, a screenshot containing multiple event details, or naturally written text descriptions of upcoming appointments, Easy ICS intelligently extracts this information and generates standard ICS (iCalendar) format files that work seamlessly with any calendar application—including Google Calendar, Outlook, Apple Calendar, and countless others.- 📅 **ICS Generation** - Generate standard calendar file format

- 🔄 **Complete Workflow** - Generate calendars from images/text in one click

The core mission of Easy ICS is to eliminate the friction between capturing calendar information in its raw form and having that information available in your digital calendar systems. In our increasingly busy world, people receive calendar information through various channels: printed schedules, email screenshots, messaging apps, handwritten notes, and more. Easy ICS bridges this gap by automating the extraction and conversion process, saving users hours of manual data entry while eliminating the potential for human error.

## 🚀 Quick Start

## The Problem We Solve

### Backend Service Setup

Modern life involves managing calendars across multiple devices and services. Students juggle class schedules from different semester sheets. Business professionals receive meeting details through emails, messages, and printed materials. Project managers coordinate teams across time zones. Yet most calendar applications still require manual data entry—a time-consuming and error-prone process that discourages many from maintaining organized schedules.

```bash

Easy ICS fundamentally changes this workflow. Instead of typing each event manually, users simply provide the source (an image or text), and the system automatically extracts structured calendar data. This approach dramatically reduces data entry time, minimizes transcription errors, and makes calendar management accessible to everyone, regardless of their comfort with technology.# Navigate to backend directory

cd backend

## Core Features

# Start development server

Easy ICS provides four interconnected capabilities that work together to create a seamless calendar conversion experience.uvicorn app.main:app --reload



**OCR Image Recognition** stands as the foundation of our image processing pipeline. The system accepts calendar images in multiple formats including PNG, JPG, JPEG, BMP, and TIFF. Using the industry-standard Tesseract OCR engine, Easy ICS extracts text from these images with remarkable accuracy. The system supports multiple languages, with particular strength in both Chinese and English—accommodating the diverse international user base. Whether you're processing a clean printout or a hastily photographed paper calendar, the OCR engine handles various layouts, formatting styles, and image qualities intelligently. This capability transforms visual information into machine-readable text, which becomes the foundation for further processing.# Access API documentation

# Open browser: http://localhost:8000/docs

**Natural Language Text Parsing** builds on the OCR output by understanding calendar information conveyed in free-form text. Users can paste or type calendar events in informal language—"Meeting tomorrow at 2pm in Room A" or "December 25 - Company holiday"—and the system automatically detects dates, times, locations, and event descriptions. The parser handles temporal references like "next Monday," "Friday afternoon," and specific dates, converting them into precise datetime values. This feature also works independently, allowing users to skip image processing entirely and directly input calendar information as text, making the tool accessible to those with scanned documents that are too degraded for OCR or users who prefer typing their calendar information.```



**ICS File Generation** takes the extracted and parsed calendar data and produces RFC 5545 compliant ICS calendar files. These files preserve all event metadata including title, start and end times, location, and description. The generation process is robust and tested, ensuring that the output files import correctly into any calendar application. Users can generate single-event or multi-event calendar files, making the tool flexible for various use cases from one-time event creation to bulk calendar import scenarios.**Detailed Guide:** 📖 [Backend Startup Guide](./docs/run.py.md)



**End-to-End Workflow Integration** brings everything together into a single, intuitive experience. The web interface presents users with a unified entry point where they can either drag and drop an image, paste a screenshot, or type calendar information. A single click triggers the entire processing pipeline—OCR extraction, event parsing, and ICS generation all happen automatically. Users receive real-time feedback about processing status and can download their calendar file with a single additional click. This streamlined workflow makes calendar conversion accessible to non-technical users while remaining powerful enough for advanced integration scenarios.### Frontend Development Server Setup



## Why Choose Easy ICS```bash

# Navigate to frontend directory

Easy ICS stands apart from alternatives in several important ways. First, there is no manual data entry required—unlike traditional calendar applications where users manually type each event, Easy ICS extracts calendar information automatically from images and text. This saves users hours of tedious typing and eliminates transcription errors that commonly occur when manually entering complex event details.cd frontend



Second, the generated calendar files are completely portable and cross-platform compatible. ICS is an international standard (RFC 5545) that works with virtually every calendar application and service. Once you generate an ICS file, you can import it into Google Calendar, Outlook, Apple Calendar, Thunderbird, or any other standards-compliant calendar system. You're never locked into a proprietary format or service.# Install dependencies

npm install

Third, Easy ICS is open source, meaning full transparency and the ability to customize the tool for your specific needs. Unlike closed-source commercial solutions, you can audit the code, understand exactly how your data is processed, and modify the system to suit your requirements. This openness builds trust and empowers users.

# Start development server

Additionally, the tool supports offline processing. You can process images and text locally on your machine without uploading sensitive calendar data to cloud servers. This addresses privacy concerns and works reliably even without internet connectivity after the initial setup.npm run dev



Finally, Easy ICS provides a developer-friendly RESTful API that enables integration into other applications and workflows. Developers can build custom applications on top of Easy ICS, incorporate it into larger systems, or create specialized tools for specific industries or use cases. The API is well-documented and easy to use, lowering barriers to integration.# Access the app

# Open browser: http://localhost:5173

## Technology Stack```



Easy ICS leverages modern, proven technologies that balance performance, maintainability, and developer experience.## 📁 Project Structure



**Backend Architecture** relies on Python 3.11 or higher, chosen for its clarity, extensive libraries, and strong community support. The backend framework is FastAPI, a modern web framework that prioritizes performance and developer productivity. FastAPI automatically generates interactive API documentation and validates request data efficiently. Data validation is handled by Pydantic, which ensures that all incoming data meets strict requirements before processing. The OCR engine is Tesseract, the industry-standard open-source solution for optical character recognition that provides excellent multilingual support. The application runs on Uvicorn, a high-performance ASGI server that handles concurrent requests efficiently.```

easy-ics/

**Frontend Architecture** uses React 19 and higher, leveraging modern hooks and features for a responsive user interface. Vite serves as the build tool, providing lightning-fast development and production builds with excellent developer experience. React Router manages client-side routing, enabling seamless navigation between the main conversion interface, project information page, and other views. CSS3 provides modern styling with smooth animations and responsive design that works beautifully on all screen sizes.├──                     # Python FastAPI backend

│   ├── app/

**Quality Assurance** includes pytest for comprehensive backend testing, ensuring reliability and catching regressions early. Docker containerization support enables consistent deployment across different environments (coming in future releases). GitHub Actions provides continuous integration infrastructure for automated testing and quality checks.│   │   ├── main.py            # Application entry point

│   │   ├── api.py             # API routes

## Prerequisites and System Requirements│   │   ├── models/            # Data models

│   │   └── services/          # Business logic

Before installing Easy ICS, ensure your system meets these requirements.│   ├── tests/                 # Unit tests

│   ├── docs/                  # Documentation

**For the Backend:** You need Python 3.11 or higher, available from python.org or your system's package manager. The pip or uv package manager is required to install Python dependencies. Tesseract OCR must be installed separately for image processing capabilities. On Windows, download the installer from the UB Mannheim repository. macOS users can install via Homebrew with `brew install tesseract`. Linux users can install via their distribution's package manager with `apt-get install tesseract-ocr` on Debian-based systems or equivalent commands on other distributions.│   ├── pyproject.toml         # Project configuration

│   └── run.py.py     # Startup script

**For the Frontend:** Node.js version 18.0 or higher is required, available from nodejs.org. The npm package manager (included with Node.js) version 9.0 or higher is needed to manage JavaScript dependencies. Alternatively, yarn or pnpm can be used as package managers.├── frontend/                   # React frontend

│   ├── src/

**System Resources:** While Easy ICS runs on modest hardware, minimum recommendations include 4GB of RAM and 500MB of disk space for dependencies. More powerful systems (8GB+ RAM, SSD storage) provide noticeably faster processing, especially when handling large images or processing many events simultaneously.│   │   ├── pages/             # Pages

│   │   ├── components/        # Components

## Installation and Setup│   │   └── App.jsx            # Main application

│   ├── package.json

Getting Easy ICS running takes approximately five minutes following these straightforward steps.│   └── vite.config.js

└── docs/                       # Project documentation

**Step 1: Clone the Repository.** Open your terminal and navigate to where you want to store the project. Run `git clone https://github.com/Q1ngX1/easy-ics.git` to download the complete project. Then navigate into the project directory with `cd easy-ics`.```



**Step 2: Set Up the Backend.** Navigate to the backend directory with `cd backend`. Install Python dependencies by running `pip install -e .` (this installs the project in editable mode) or `uv sync` if you prefer the uv package manager. Once installation completes, start the development server with `uvicorn app.main:app --reload`. The backend will start at `http://localhost:8000`. The `--reload` flag enables automatic server restart when code changes, perfect for development. Leave this terminal window open.## 🛠️ Tech Stack



**Step 3: Set Up the Frontend.** Open a new terminal window and navigate to the frontend directory with `cd frontend`. Install JavaScript dependencies with `npm install`. This step downloads and installs all required packages from npm. Once installation completes, start the development server with `npm run dev`. The frontend will start at `http://localhost:5173`.### Backend

- **FastAPI** - Modern web framework

**Step 4: Access the Application.** Open your web browser and navigate to `http://localhost:5173`. You should see the Easy ICS interface with the image upload area and text input field. Both backend and frontend are now running and ready to process calendar information. The development servers support hot reload, so changes to code appear immediately without requiring restarts.- **Pydantic** - Data validation

- **Tesseract OCR** - Image recognition

## Usage Guide- **Python 3.11+** - Programming language



Easy ICS provides an intuitive web interface complemented by powerful API endpoints for programmatic access.### Frontend

- **React** - UI framework

**Using the Web Interface** requires minimal technical knowledge. Start by accessing the main page at your running frontend URL. You have three options for input. First, you can drag and drop an image directly onto the designated area on the page. Second, you can click the upload area to browse your file system and select an image. Third, you can copy an image to your clipboard and paste it directly into the page using Ctrl+V (or Command+V on macOS). Alternatively, you can skip image processing entirely and type or paste calendar event text directly into the text input field. Once you've provided input, click the "Convert" button. The application processes your input and displays the results within seconds. If processing succeeds, you'll see a message indicating how many events were detected. Simply click the "Download ICS" button to download your calendar file. The downloaded file is ready to import into any calendar application.- **Vite** - Build tool

- **CSS3** - Styling

**Using the API Programmatically** provides additional flexibility for developers and advanced users. The API accepts JSON requests over HTTP and returns structured responses. To upload an image for OCR processing, send a POST request to `/api/upload/img` with the image as form data. The response includes the extracted text and metadata about the image. To parse text and extract calendar events, send a POST request to `/api/upload/text` with the text as a query parameter. The response includes an array of detected events with their parsed details. To download a calendar file, send a POST request to `/api/download_ics` with a JSON body containing the events array. The response is a binary ICS file ready for download or further processing.

## 📚 Documentation

**Example Usage:** Suppose you want to extract events from a screenshot of a calendar. Using curl (a command-line tool for making HTTP requests), you could run: `curl -X POST "http://localhost:8000/api/upload/img" -F "file=@screenshot.png"`. The system responds with the extracted text. You then parse this text by running: `curl -X POST "http://localhost:8000/api/upload/text" -d "text=extracted_calendar_text"`. The system responds with structured events. Finally, you download the calendar file by running a POST request to `/api/download_ics` with the events, and the system returns a complete ICS file.

| Document | Description |

## API Documentation|----------|-------------|

| [Backend Startup Guide](./docs/run.py.md) | How to start backend service and use startup script |

The Easy ICS API is fully documented and interactive, making integration straightforward.| [Backend README](./README.md) | Detailed backend project documentation |

| [ICS Service Documentation](./docs/ICS_SERVICE.md) | Complete ICS file generation and parsing documentation |

**Interactive API Documentation** is automatically generated by FastAPI. Once your backend is running, visit `http://localhost:8000/docs` to access the Swagger UI interface. This interactive documentation shows every available endpoint, their parameters, request/response formats, and allows you to test endpoints directly in your browser without writing any code. Alternative documentation in ReDoc format is available at `http://localhost:8000/redoc`.| [ICS Quick Reference](./docs/ICS_SERVICE_QUICK_REFERENCE.md) | ICS service common methods quick reference |

| [Frontend README](./frontend/README.md) | Frontend project documentation |

**Health Check Endpoint** at `GET /api/check_health` verifies that the backend is running and that all required services are available. The response includes the system status and whether Tesseract OCR is properly installed and accessible.

## 🔧 Requirements

**Image Upload Endpoint** at `POST /api/upload/img` accepts image files in PNG, JPG, JPEG, BMP, or TIFF format. The system runs OCR to extract text from the image. The response includes the extracted text, the original filename, the length of extracted text, and a success status. Optional query parameter `lang` specifies the OCR language (default is "chi_sim+eng" for Chinese simplified and English).

### Backend

**Text Parsing Endpoint** at `POST /api/upload/text` accepts calendar event text as a query parameter. The system parses the text to identify events, dates, times, locations, and descriptions. The response includes an array of extracted events with their properties and a count of detected events. Optional query parameter `lang` specifies the parsing language.- Python >= 3.11

- pip or uv package manager

**ICS Download Endpoint** at `POST /api/download_ics` accepts a JSON body containing an array of event objects. Each event should include title, start_time, end_time, and optionally location and description. The system generates an RFC 5545 compliant ICS file and returns it as a downloadable binary stream. The response includes appropriate headers to trigger file download in browsers.- Tesseract OCR (optional, for image recognition)



## Project Structure and Architecture### Frontend

- Node.js >= 18

Understanding the project organization helps both users and developers navigate the codebase effectively.- npm or yarn



The backend resides in the `backend/` directory and contains the Python FastAPI application. The `app/main.py` file serves as the application entry point, setting up the FastAPI instance and initializing services. The `app/api.py` file defines all route endpoints that handle incoming requests. The `app/models/` directory contains Pydantic data models that define the structure of events and other data objects. The `app/services/` directory contains the business logic: `ocr_service.py` handles image text extraction using Tesseract, `parser_service.py` contains logic for extracting calendar information from text, and `ics_service.py` handles ICS file generation. The `tests/` directory contains unit tests that verify correctness of all major components. The `pyproject.toml` file specifies all project dependencies and configuration details.## ⚙️ Install Dependencies



The frontend resides in the `frontend/` directory and contains the React application built with Vite. The `src/pages/` directory contains page components: `Home.jsx` provides the main conversion interface with image upload and text input, `About.jsx` displays project information, and `NotFound.jsx` handles 404 errors for non-existent routes. The `src/services/apiService.js` file provides all functions for communicating with the backend API. The `src/styles/pages.css` file contains all CSS styling for consistent appearance. The `src/App.jsx` file provides the main application component with routing configuration. The `package.json` file specifies JavaScript dependencies and build scripts.### Backend



The `docs/` directory contains additional documentation including API references and architecture documentation. The root `README.md` (this file) provides project overview and getting started information.```bash

cd backend

## Development Workflow

# Option 1: Using pip

For developers wanting to contribute to Easy ICS or customize the tool, setting up a development environment is straightforward.pip install -e .



**Backend Development Setup** begins by creating a Python virtual environment to isolate dependencies: `python -m venv venv`. Activate it with `source venv/bin/activate` on macOS/Linux or `venv\Scripts\activate` on Windows. Install development dependencies with `pip install -e ".[dev]"`. This installs the project in editable mode with development tools included. Start the development server with `uvicorn app.main:app --reload`, which automatically restarts the server when Python files change.# Option 2: Using uv

uv sync

**Frontend Development Setup** requires installing Node.js dependencies with `npm install`. Start the development server with `npm run dev`. The Vite development server provides hot module replacement, meaning changes to React components instantly appear in the browser without full page reloads. Both TypeScript and JSX errors appear in the terminal and browser console, helping catch issues immediately during development.```



**Running Tests** ensures code quality and prevents regressions. For the backend, run `pytest tests/ -v` to execute all tests with verbose output. Run `pytest tests/ --cov=app --cov-report=html` to generate a coverage report showing which parts of the code are tested. For the frontend, run `npm run test` to execute tests in your JavaScript environment.### Frontend



**Building for Production** requires different steps than development. For the backend, use `uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4` to run a production server with multiple worker processes for handling concurrent requests. For the frontend, run `npm run build` to create an optimized production build in the `dist/` directory. This directory can then be deployed to any static web server.```bash

cd frontend

## Real-World Examplesnpm install

```

Several practical scenarios illustrate Easy ICS capabilities and demonstrate how the tool solves real problems.

## 📡 API Endpoints

**Example 1: Digitizing a Paper Schedule.** Imagine you have a printed semester course schedule or a hand-written event calendar. Photograph this document with your smartphone. Open Easy ICS and drag the image to the upload area. Within seconds, the system extracts all event text from the photo. Click "Download ICS" and you now have a calendar file containing all your courses or events. Import this file into your phone's calendar application or email it to a colleague—they instantly have access to the complete schedule without any manual transcription.

After starting the backend service, visit http://localhost:8000/docs to view the complete interactive API documentation.

**Example 2: Processing Event Email.** You receive an email with meeting details—"Next Monday 10am - Team standup in Conference Room A, Friday 3pm - Project deadline, December 25 - Company holiday." Rather than manually entering each event, copy this text and paste it into Easy ICS. The system automatically detects three distinct events with their dates and times. Download the ICS file and import it into your calendar. All events appear at the correct times, and you've saved yourself several minutes of manual entry while eliminating potential transcription errors.

**Main Endpoints:**

**Example 3: Programmatic Calendar Integration.** A developer wants to incorporate Easy ICS into a larger scheduling application. They use the REST API to send event data to the `/api/download_ics` endpoint and receive calendar files that their application can then distribute to users. This capability enables powerful use cases like automatically generating calendar exports when users complete event registration, or creating calendar files from scheduling system data.- `GET /api/check_health` - Health check

- `POST /api/upload/img` - Upload image for OCR recognition

## Contributing to Easy ICS- `POST /api/upload/text` - Parse text to extract events

- `POST /api/download_ics` - Generate ICS file

We welcome contributions from developers, designers, and documentation writers at all experience levels. Your perspective and efforts help make Easy ICS better for everyone.

## 🧪 Testing

**Reporting Issues** should be done through GitHub Issues. When reporting a bug, provide a clear description of what you were trying to do, steps to reproduce the issue, what you expected to happen, and what actually happened instead. Including screenshots or code examples significantly helps the maintainers understand and fix the issue quickly. For feature requests, clearly describe the desired functionality and explain the problem it would solve or the improvement it would provide.

### Backend Tests

**Submitting Code Contributions** follows a standard workflow that respects the project's quality standards. Fork the repository to create your own copy. Create a feature branch with a descriptive name like `feature/improve-ocr-accuracy` or `fix/calendar-import-issue`. Make your changes and test them thoroughly to ensure they work correctly. Commit your changes with clear, descriptive messages explaining what you changed and why those changes are beneficial. Push your branch to your fork and open a pull request on the main repository with a detailed description of your changes. Respond thoughtfully to any review feedback, make requested adjustments, and ensure all tests pass before maintainers merge your contribution.

```bash

**Development Guidelines** help maintain code quality and consistency across the project. For Python code, follow PEP 8 style guidelines to keep code readable and consistent with Python conventions. For JavaScript and React, adhere to the ESLint rules configured in the project. Always add tests for new features—untested code is difficult to maintain and refactor. Update documentation when adding functionality so other developers understand how to use new features. Keep commits atomic, meaning each commit represents a single logical change that can be understood and reviewed independently.cd backend



## Maintainers and Project Support# Run all tests

pytest tests/ -v

Easy ICS is actively maintained by a dedicated team committed to the project's success and the satisfaction of its users.

# Run specific test class

The primary maintainer is Q1ngX1, who oversees the project vision, coordinates contributions from the community, and ensures code quality remains high. You can find them on GitHub at [Q1ngX1](https://github.com/Q1ngX1). For questions about project direction, major architectural decisions, or long-term planning, opening an issue or discussion is the best approach to get their attention and input.pytest tests/ics_service_test.py -v



## Version History and Development Roadmap# Generate coverage report

pytest tests/ --cov=app --cov-report=html

Understanding the project's evolution and future direction helps users make informed decisions about adoption and potential use cases.```



**Version 0.1.0 (Current Release - November 2025)** represents the initial release establishing core functionality. This version includes OCR image recognition for accurate text extraction from calendar images, text parsing to identify calendar events from natural language descriptions, ICS file generation producing RFC 5545 compliant calendar files, a web interface for intuitive user interaction, and RESTful API endpoints enabling programmatic access. This version establishes the solid foundation on which all future development will build.### Frontend Tests



**Version 0.2.0 (Planned for Early 2026)** will enhance text parsing capabilities to better understand complex calendar descriptions and ambiguous date references, include comprehensive integration tests covering entire workflows from image upload through ICS file download, provide Docker containerization for dramatically simplified deployment across different environments, and optimize performance for handling large batch operations and high-concurrency scenarios where many users access the system simultaneously.```bash

cd frontend

**Version 1.0.0 (Planned for Mid-2026)** will add support for recurring events with patterns like "every Tuesday at 2pm" or "monthly on the 15th", enable exporting to multiple calendar formats simultaneously from a single extraction, include user authentication and personal calendars allowing users to save and manage their calendar conversions, provide event history tracking showing previous conversions and modifications, and potentially include native mobile applications for iOS and Android platforms.

# Run tests

Beyond version 1.0.0, the roadmap includes more sophisticated recurring event patterns, collaborative calendar sharing among multiple users, calendar synchronization with external services like Google Calendar, advanced machine learning to improve event extraction accuracy, and integrations with popular calendar services and communication platforms.npm run test

```

## License and Legal Information

## 🐛 FAQ

Easy ICS is distributed under the MIT License, one of the most permissive open source licenses available today. This choice reflects our commitment to accessibility and freedom.

**Q: How to start the development environment?**

The MIT License grants you permission to use this software for any purpose, including commercial applications where you sell software or services incorporating Easy ICS. You can modify the code for your specific needs and requirements. You can distribute the software to others, either in its original form or modified versions. The only requirements are that you include the original license and copyright notice in any distribution, and that you acknowledge that the software is provided "as is" without any warranty. The maintainers accept no liability for issues arising from use of the software.

A: Run the following commands:

This permissive approach reflects our belief that tools for solving real problems should be accessible to everyone. Whether you're using Easy ICS for personal projects, in a classroom setting, for non-profit work, or as part of commercial software, the MIT License provides the freedom to do so without restrictions.```bash

# Backend

## Getting Help and Supportcd backend && uvicorn app.main:app --reload



Comprehensive support is available through multiple channels to help you succeed with Easy ICS.# Frontend (new terminal)

cd frontend && npm run dev

**Documentation** resources include the main README file you're currently reading, detailed API documentation available at `http://localhost:8000/docs` when your backend is running (allowing you to test endpoints interactively), architecture documentation and guides in the `docs/` folder, and tutorial guides for common use cases. Start here if you're learning to use Easy ICS or need reference information.```



**GitHub Issues** is the primary way to report bugs, suggest features, or ask questions about using the tool. Search existing issues first—your question or issue may already be answered, and you can read the discussion and solution. When opening a new issue, provide sufficient context and details that help maintainers understand and address the problem quickly without requiring follow-up questions.**Q: How to test the API?**



**Common Issues and Solutions:** If the backend fails to start, verify that Python 3.11 or higher is installed on your system and that all dependencies are installed correctly with `pip install -e .`. If OCR functionality doesn't work, ensure Tesseract is installed on your system—download the Windows installer from the UB Mannheim repository, use `brew install tesseract` on macOS, or `apt-get install tesseract-ocr` on Linux. If ports are already in use by other applications, specify different ports: for the backend, add `--port 8001` to the uvicorn command; for the frontend, use `npm run dev -- --port 5174`. If the frontend shows a blank page, check the browser console (open with F12) for errors, verify the backend is running and accessible, and check network requests to ensure API communication works correctly.A: After starting the backend, visit http://localhost:8000/docs and use Swagger UI to test



## Acknowledgments**Q: How to install Tesseract?**



Easy ICS builds on the work of many talented individuals and teams in the open source community, and we're grateful for their contributions.A: Refer to the installation guide in [Backend README](./README.md#-install-dependencies)



We thank the Tesseract OCR team for developing and maintaining the industry-standard optical character recognition engine that powers our image processing. We appreciate the FastAPI team for creating such a productive and performant web framework that enabled rapid development. The React and Vite communities have provided exceptional tools and ongoing support that enhanced our frontend development. We're grateful to all contributors who have reported issues, suggested improvements, and submitted code that makes Easy ICS better with each release. Finally, we thank our users who provide valuable feedback and help us understand how to make calendar processing simpler and more accessible.## 📖 Usage Examples



## Related Resources and Further Reading### Generate ICS File from Text



To deepen your understanding of Easy ICS and its underlying technologies, several resources prove valuable and educational.```python

from app.services.ics_service import ICSService

The ICS/iCalendar format specification is formally defined in RFC 5545, available at [https://tools.ietf.org/html/rfc5545](https://tools.ietf.org/html/rfc5545). Understanding this standard helps you appreciate what Easy ICS generates and how to work with calendar files in other contexts. Tesseract OCR documentation at [https://github.com/UB-Mannheim/tesseract/wiki](https://github.com/UB-Mannheim/tesseract/wiki) provides detailed information about the OCR engine and advanced configuration options. The FastAPI documentation at [https://fastapi.tiangolo.com/](https://fastapi.tiangolo.com/) offers comprehensive guides for understanding the backend framework and building similar systems. The React documentation at [https://react.dev/](https://react.dev/) provides thorough explanations of concepts used in the frontend. These resources deepen your knowledge and enable more advanced customization if needed.from app.models.event import Event

from datetime import datetime

## Project Status and Maintenance

# Create event

Easy ICS is actively developed and maintained by its community. New features are regularly added based on user requests, bugs are promptly addressed when discovered, and the codebase stays current with modern development practices and security standards. This is not an abandoned or legacy project—it continues to evolve based on user feedback, technological improvements, and emerging best practices in both Python and JavaScript ecosystems. Users can trust that their investment in learning and using Easy ICS will be rewarded by ongoing support and improvements.event = Event(

    title="Project Meeting",

---    start_time=datetime(2025, 10, 26, 14, 0),

    end_time=datetime(2025, 10, 26, 15, 0),

**Made with ❤️ by the Easy ICS Team**    location="Meeting Room A"

)

Last Updated: November 7, 2025

# Generate ICS
service = ICSService()
ics_content = service.generate_ics([event])

# Save file
with open("calendar.ics", "w") as f:
    f.write(ics_content)
```

### Generate Calendar Using API

```bash
curl -X POST "http://localhost:8000/api/download_ics" \
  -H "Content-Type: application/json" \
  -d '{
    "events": [
      {
        "title": "Project Meeting",
        "start_time": "2025-10-26T14:00:00",
        "end_time": "2025-10-26T15:00:00"
      }
    ]
  }' \
  --output calendar.ics
```

## 🚀 Deployment

### Docker Deployment (Coming Soon)

```bash
docker-compose up
```

### Production Deployment

Backend:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Frontend:
```bash
npm run build
# Deploy dist directory to static server
```

## 📝 Development Roadmap

- [x] Project structure setup
- [x] Backend framework initialization
- [x] OCR service implementation
- [x] ICS generation service
- [x] ICS parsing service
- [x] Basic API routes
- [x] Frontend page optimization
- [ ] Text parsing service
- [ ] Complete integration tests
- [ ] Docker deployment configuration
- [ ] Production environment optimization

## 🤝 Contributing

Issues and Pull Requests are welcome!

## 📄 License

MIT License - See LICENSE file for details

## 💬 Contact

- GitHub Issues: [Project Issue Tracking](../../issues)
- Project Homepage: [GitHub](https://github.com/Q1ngX1/easy-ics)

---

**Made with ❤️ by the Easy ICS Team** 