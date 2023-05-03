import { useState } from "react";
import './css code/Thirdform.css';

function Thirdform(props) {
    const [focused, setFocused] = useState(false);
    const { label, errorMessage, onChange, id, ...inputProps } = props;

    const handleFocus = (e) => {
        setFocused(true);
    };

    return (
        <div className="container">
            <div className="app-wrapper">
                <label>{label}</label>
                <input className="input2"
                    {...inputProps}
                    onChange={onChange}
                    onBlur={handleFocus}
                    onFocus={() => inputProps.name === "confirmPassword" && setFocused(true)}
                    focused={focused.toString()} />
                <span>{errorMessage}</span>
            </div>
        </div>
    );
}

export default Thirdform ;
