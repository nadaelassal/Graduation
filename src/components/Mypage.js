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
import SettingsIcon from "@mui/icons-material/Settings";
import ReplyIcon from "@mui/icons-material/Reply";
import "./css code/Mypage.css";
import "./Nav2";
import Nav from "./Nav2";
import { Container } from "@mui/material";
import profile from './pro.png';


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
      <Nav />

      <Container className="mycontainer">
        <Box
          sx={{
            flexGrow: 1,
            display: "flex",
            height: 550,
            bgcolor: "#1111",
            borderRadius: 25,
            width: 50,
            marginLeft: -20,
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
            <Tab icon={<HomeIcon />} {...a11yProps(0)} />
            <br />
            <Tab icon={<PlaceIcon />} {...a11yProps(1)} />
            <br />
            <Tab icon={<AccountCircleIcon />} {...a11yProps(2)} />
            <br />
            <Tab icon={<SettingsIcon />} {...a11yProps(3)} />
            <br />
            <Tab icon={<ReplyIcon />} {...a11yProps(4)} />
          </Tabs>
          <TabPanel value={value} index={0}>
            Hi
          </TabPanel>
          <TabPanel value={value} index={2}>
            Hello
          </TabPanel>
          <TabPanel value={value} index={4}>
          
          </TabPanel>
          <TabPanel value={value} index={6}>
            be
          </TabPanel>
          <TabPanel value={value} index={8}>
            no
          </TabPanel>
        </Box>
      </Container>
    </div>
  );
}
