/* eslint-disable jsx-a11y/alt-text */
/* eslint-disable react/jsx-no-undef */
import * as React from "react";
import PropTypes from "prop-types";
import Tabs from "@mui/material/Tabs";
import Tab from "@mui/material/Tab";
import Typography from "@mui/material/Typography";
import Box from "@mui/material/Box";
import HomeIcon from "@mui/icons-material/Home";
import PlaceIcon from "@mui/icons-material/Place";
import AccountCircleIcon from "@mui/icons-material/AccountCircle";
import ReplyIcon from "@mui/icons-material/Reply";
import "./css code/Mypage.css";
import Nav2 from "./Nav2";
import { Container } from "@mui/material";
import HomeTab from "./HomeTab";
import Map from "./Map";
import { Link } from "react-router-dom";
import ProfileTab from "./Profiletab";

function TabPanel(props) {
  const { children, value, index, ...other } = props;

  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`vertical-tabpanel-${index}`}
      aria-labelledby={`vertical-tab-${index}`}
      {...other}
    >
      {value === index && (
        <Box sx={{ p: 3 }}>
          <Typography>{children}</Typography>
        </Box>
      )}
    </div>
  );
}

TabPanel.propTypes = {
  children: PropTypes.node,
  index: PropTypes.number.isRequired,
  value: PropTypes.number.isRequired,
};

function a11yProps(index) {
  return {
    id: `vertical-tab-${index}`,
    "aria-controls": `vertical-tabpanel-${index}`,
  };
}

export default function VerticalTabs() {
  const [value, setValue] = React.useState(0);

  const handleChange = (event, newValue) => {
    setValue(newValue);
  };

  return (
    <div>
      <Nav2/>

      <Container className="mycontainer">
        <Box
          sx={{
            flexGrow: 1,
            display: "flex",
            height: 550,
            bgcolor: "#1111",
            borderRadius: 25,
            width: 50,
            marginLeft: -18,
            marginTop: 10,
          }}
        >
          <Tabs
            orientation="vertical"
            variant="scrollable"
            value={value}
            onChange={handleChange}
            aria-label="Vertical tabs "
            className="tabs"
          >
            <Tab
              icon={<HomeIcon />}
              {...a11yProps(0)}
              style={{ minWidth: "50%" }}
            />
            <br />
            <Tab
              icon={<PlaceIcon />}
              {...a11yProps(1)}
              style={{ minWidth: "50%" }}
            />
            <br />
            <Tab
              icon={<AccountCircleIcon />}
              {...a11yProps(2)}
              style={{ minWidth: "50%" }}
            />
            <br />
            <Link to="/Content">
              <Tab
                icon={<ReplyIcon />}
                {...a11yProps(3)}
                
              />
            </Link>
          </Tabs>
        </Box>
      </Container>
      <TabPanel value={value} index={0} className="panel1">
        <HomeTab />
      </TabPanel>
      <TabPanel value={value} index={2} className="panel2">
        <Map />
      </TabPanel>
      <TabPanel value={value} index={4} className="panel3"><ProfileTab/></TabPanel>
    </div>
  );
}
