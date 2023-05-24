/*import "./css code/forgetcode.css";
import ArrowBackOutlinedIcon from "@mui/icons-material/ArrowBackOutlined";
import { Link, useNavigate } from "react-router-dom";
import Box from "@mui/material/Box";
import TextField from "@mui/material/TextField";
import React, { useState } from "react";

function Forgetcode() {
  const [number, setNumber] = useState("");
  const [errors, setErrors] = useState({});

  const navigate = useNavigate();

  const validateNumber = (value) => {
    const numberPattern = "";
    return numberPattern.test(value);
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    const newErrors = {};

    if (!validateNumber(number)) {
      newErrors.email = "Invalid code ";
    }

    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors);
    } else {
      // signup successful, navigate to home page
      navigate("/Forget2");
    }
  };

  return (
    <div>
      <Link to="/Forget" className="backbutton000">
        <ArrowBackOutlinedIcon fontSize="large" className="backbutton000" />
      </Link>

      <div className="code">
        <h1 className="co">CO</h1>
        <h1 className="de">DE</h1>
      </div>
      <h1 className="verfiy">Verfication</h1>

      <form onSubmit={handleSubmit}>
        <Box
          component="form"
          sx={{
            "& > :not(style)": { m: 2, width: "50px" },
          }}
          noValidate
          autoComplete="off"
          marginLeft={70}
          marginTop={2}
          className="box"
          onChange={(e) => setNumber(e.target.value)}
        >
          <TextField id="first" className="textfeild" />
          <TextField id="sec" className="textfeild" />
          <TextField id="third" className="textfeild" />
          <TextField id="fourth" className="textfeild" />
          <TextField id="fifth" className="textfeild" />
          {errors.number && <div className="error">{errors.number}</div>}
        </Box>
        
      </form>
      <div>
          <button type="submit" className="button-container-Nextforget">
            Next
          </button>
        </div>
    </div>
  );
}
export default Forgetcode;
*/
import "./css code/forgetcode.css";
import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Pattern } from "@mui/icons-material";
import ArrowBackOutlinedIcon from "@mui/icons-material/ArrowBackOutlined";
import { Link } from "react-router-dom";
import Box from "@mui/material/Box";
import TextField from "@mui/material/TextField";

function Forgetcode() {
  const [number, setNumber] = useState("");
  const [errors, setErrors] = useState({});
  const navigate = useNavigate();

  const validateNumber = (value) => {
    const numberPattern = /[0-9]/;
    return numberPattern.test(value);
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    const newErrors = {};

    if (!validateNumber(number)) {
      newErrors.email = "Invalid code ";
    }

    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors);
    } else {
      // signup successful, navigate to home page
      navigate("/Forget2");
    }
  };

  return (
    <div>
      <Link to="/Forget" className="backbutton000">
        <ArrowBackOutlinedIcon fontSize="large" className="backbutton000" />
      </Link>

      <div className="code">
        <h1 className="co">CO</h1>
        <h1 className="de">DE</h1>
      </div>
      <h1 className="verfiy">Verfication</h1>
      <form onSubmit={handleSubmit}>
        <div className="box">
          <Box
            component="form"
            sx={{
              "& > :not(style)": { m: 2, width: "50px" },
            }}
            noValidate
            autoComplete="off"
            marginLeft={70}
            marginTop={2}
            value={number}
            onChange={(e) => setNumber(e.target.value)}
            required
            className="box"
          >
            <TextField id="first" className="textfeild" />
            <TextField id="sec" className="textfeild" />
            <TextField id="third" className="textfeild" />
            <TextField id="fourth" className="textfeild" />
            <TextField id="fifth" className="textfeild" />

            {errors.number && <div className="error">{errors.number}</div>}
          </Box>
        </div>

        <div>
          <button type="submit" className="button-container-Nextforget">
            Next
          </button>
        </div>
      </form>
      <h1 className="resend">Resend code ?</h1>
    </div>
  );
}

export default Forgetcode;
