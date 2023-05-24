import React from "react";
import ReactDOM from "react-dom";
import "./components/index.css";
import App from "./App";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Guides from "./components/Guides";
import Help from "./components/Help";
import SignUp from "./components/SignUp";
import Signin from "./components/Signin";
import Forget from "./components/Forget";
import Forget2 from "./components/Forget2";
import Home from "./components/Home";
import Nav from "./components/Nav";
import SignUp2 from "./components/Signup2";
import Mypage from "./components/Mypage";
import Content from "./components/Content";
import Forgetcode from "./components/Forgetcode";
import Signiformation from './components/Signiformation';


ReactDOM.render(
  <Router>
    <Routes>
      <Route path="/" element={<App />} />
      <Route path="/Guides" element={<Guides />} />
      <Route path="/Help" element={<Help />} />
      <Route path="/Home" element={<Home/>} />
      <Route path="/Signup2" element={<SignUp2/>} />
      <Route path="/Nav" element={<Nav />} />
      <Route path="/SignUp" element={<SignUp/>} />
      <Route path="/Signiformation" element={<Signiformation/>} />
      <Route path="/Signin" element={<Signin/>} />
      <Route path="/Forget" element={<Forget/>} />
      <Route path="/Forget2" element={<Forget2/>} />
      <Route path="/Mypage" element={<Mypage/>}/>
      <Route path="/content" element={<Content/>}/>
      <Route path="/Forgetcode" element={<Forgetcode/>}/>
 

    </Routes>
  </Router>,
  document.getElementById("root")
);
