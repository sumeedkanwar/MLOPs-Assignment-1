# MLOps CI/CD Pipeline - Car Price Prediction 🚗

A comprehensive MLOps pipeline implementing CI/CD best practices for a machine learning application that predicts car prices using PakWheels dataset.

## 🎯 Project Overview

This project demonstrates a complete MLOps CI/CD pipeline with:
- **ML Model**: Random Forest Regressor for car price prediction
- **Dataset**: PakWheels car price data (unique to our group)
- **API**: Flask REST API for model serving
- **Pipeline**: Automated CI/CD with GitHub Actions and Jenkins
- **Containerization**: Docker for deployment
- **Quality Assurance**: Automated testing and code quality checks

## 🏗️ Architecture

```
Dev Branch → Test Branch → Main Branch
    ↓           ↓            ↓
  Flake8    Unit Tests   Jenkins Pipeline
                            ↓
                    Docker Hub + Email Notification
```

## 🔄 CI/CD Pipeline Workflow

### 1. **Development Phase**
- Developers push code to `dev` branch
- **GitHub Action**: Code quality check with `flake8`
- Admin reviews and approves pull request

### 2. **Testing Phase**
- Features merged from `dev` → `test` branch
- **GitHub Action**: Automated unit testing with `pytest`
- Tests must pass before proceeding

### 3. **Production Deployment**
- Code merged from `test` → `main` branch
- **Jenkins Pipeline**:
  - Code checkout
  - Lint & test validation
  - Docker image build
  - Push to Docker Hub
  - Email notification to admin

## 📂 Project Structure

```
├── .github/workflows/          # GitHub Actions workflows
│   ├── flake8.yml             # Code quality check (dev branch)
│   ├── unittest.yml           # Unit testing (test branch)
│   └── deploy.yml             # Deployment trigger (main branch)
├── app/                       # Application source code
│   ├── api.py                 # Flask REST API
│   ├── model.py               # ML model training
│   └── preprocess.py          # Data preprocessing
├── data/raw/                  # Dataset
│   └── pakwheels.csv          # Car price dataset
├── tests/                     # Test suite
│   ├── test_api.py            # API tests
│   └── test_preprocess.py     # Preprocessing tests
├── artifacts/                 # Model artifacts
├── Dockerfile                 # Container configuration
├── Jenkinsfile               # Jenkins pipeline definition
├── requirements.txt          # Python dependencies
└── run.py                   # Application entry point
```

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Docker
- Jenkins (configured)
- GitHub repository with Actions enabled

### Local Development

1. **Clone Repository**
   ```bash
   git clone https://github.com/sumeedkanwar/MLOPs-Assignment-1.git
   cd MLOPs-Assignment-1
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Train Model**
   ```bash
   python app/model.py
   ```

4. **Run Application**
   ```bash
   python run.py
   ```

5. **Test API**
   ```bash
   curl -X POST http://localhost:5000/predict \
     -H "Content-Type: application/json" \
     -d '{"age": 5, "mileage": 50000, "fuel_type": "Petrol", "transmission": "Automatic", "city": "Lahore", "registered": "Lahore", "assembly": "Local"}'
   ```

### Docker Deployment

1. **Build Image**
   ```bash
   docker build -t mlops-car-price .
   ```

2. **Run Container**
   ```bash
   docker run -p 5000:5000 mlops-car-price
   ```

## 🔧 Pipeline Configuration

### Branch Protection Rules

To enable the CI/CD workflow, configure these branch protection rules:

#### Main Branch
- ✅ Require pull request reviews before merging
- ✅ Require status checks to pass before merging
- ✅ Require branches to be up to date before merging
- ✅ Include administrators in restrictions

#### Test Branch
- ✅ Require pull request reviews before merging
- ✅ Require status checks to pass before merging

#### Dev Branch
- ✅ Require status checks to pass before merging

### Jenkins Setup

1. **Install Required Plugins**
   - GitHub Plugin
   - Docker Pipeline Plugin
   - Email Extension Plugin

2. **Configure Credentials**
   - Add Docker Hub credentials as `docker-hub-creds`
   - Configure email SMTP settings

3. **Create Pipeline Job**
   - Use `Jenkinsfile` from repository
   - Configure webhook for automatic triggers

### GitHub Secrets (Optional for Jenkins Integration)

```
JENKINS_URL=https://your-jenkins-server.com
JENKINS_USER=your-username
JENKINS_TOKEN=your-api-token
```

## 🧪 Testing

### Run All Tests
```bash
pytest tests/ -v
```

### Code Quality Check
```bash
flake8 app tests --max-line-length=120
```

## 📊 Model Performance

- **Algorithm**: Random Forest Regressor with hyperparameter tuning
- **Features**: Car age, mileage, fuel type, transmission, city, registration status, assembly
- **Target**: Car price prediction (PKR)
- **Preprocessing**: Log transformation, categorical encoding
- **Validation**: R² score and RMSE on test set

## 👥 Team Members

- **Member 1**: [Your Name] - Model Development & API Implementation
- **Member 2**: [Partner Name] - Pipeline Configuration & Testing
- **Admin**: sumeedkanwar@gmail.com

## 📋 Assignment Compliance

✅ **Required Tools Used**
- Jenkins ✓
- GitHub ✓  
- GitHub Actions ✓
- Git ✓
- Docker ✓
- Python ✓
- Flask ✓

✅ **Pipeline Features**
- Admin approval process ✓
- Code quality checks (flake8) ✓
- Automated unit testing ✓
- Branch-based workflow (dev → test → main) ✓
- Jenkins containerization ✓
- Docker Hub deployment ✓
- Email notifications ✓

## 🔗 Links

- **GitHub Repository**: https://github.com/sumeedkanwar/MLOPs-Assignment-1
- **Docker Hub**: https://hub.docker.com/r/sumeedkanwar/mlops-assignment-1
- **Jenkins Dashboard**: [Configure your Jenkins URL]

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.