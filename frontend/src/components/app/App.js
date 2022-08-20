import './App.css';
import LoginForm from '../LoginForm/LoginForm';
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

function App() {
  return (
    <div className="App">
       <Router>
          <Routes>
            <Route exact path="/" element={<LoginForm />} />
          </Routes>
      </Router>
    </div>
  );
}

export default App;
