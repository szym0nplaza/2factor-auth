import "./App.css";
import LoginForm from "../LoginForm/LoginForm";
import AuthForm from "../AuthForm/AuthForm";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import HomePage from "../HomePage/HomePage";

function App() {
  return (
    <div className="App">
      <Router>
        <Routes>
          <Route exact path="/" element={<LoginForm />} />
          <Route path="/verification" element={<AuthForm />} />
          <Route path="/home" element={<HomePage />} />
        </Routes>
      </Router>
    </div>
  );
}

export default App;
