/* eslint-disable jsx-a11y/alt-text */
import "./css code/signiformation.css";
import sign from "./signup2.jpg";
import { useNavigate } from "react-router-dom";

function Signiformation() {
    const navigate = useNavigate();
  return (
    <div>
      <img src={sign} className="sign2img" />
      <h1 className="wel">Welcome MR Ali</h1>

      <h3 className="ph">
        please fill this fields <br />
        so we can help you more
      </h3>

      <div className="input-holder101">
        <input
          className="input-holder101"
          type="hight"
          name="hight"
          placeholder="Enter Your Hight"
          value={Number}
          required
        />
      </div>

      <div className="input-holder202">
        <input
          className="input-holder202"
          type="Weight"
          name="Weight"
          placeholder="Enter Your Weight"
          value={Number}
          required
        />
      </div>

      <div className="input-holder303">
        <input
          className="input-holder303"
          type="Age"
          name="Age"
          placeholder="Enter Your Age"
          value={Number}
          required
        />
      </div>

      <button
        type="submit"
        className="button-confirm1"
        onClick={() => navigate("/Signup2")}
      >
        Confirm
      </button>
    </div>
  );
}
export default Signiformation;
