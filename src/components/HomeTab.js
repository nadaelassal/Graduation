/* eslint-disable jsx-a11y/alt-text */
import { Container } from "@mui/material";
import Box from "@mui/material/Box";
import PieChartComponent from "./bichart";
import BarChartComponent from "./barcharts";
import "./css code/hometab.css";
import MultiActionAreaCard from "./Card1";
import MultiActionAreaCard2 from "./Card2";
import MultiActionAreaCard3 from "./Card3";
import ach from "./ach.jpg";
import Card from "@mui/material/Card";
import CardContent from "@mui/material/CardContent";
import CardMedia from "@mui/material/CardMedia";
import Typography from "@mui/material/Typography";
import Percent from "./percent";

const HomeTab = () => {
  return (
    <div>
      <Container>
        <Box
          sx={{
            flexGrow: 1,
            display: "flex",
            height: 230,
            borderRadius: 5,
            width: 380,
            marginLeft: 2,
            marginTop: -70,
            boxShadow: 10,
          }}
        >
          <h3 className="BMI">BMI Calculator </h3>
          <div className="pie">
            <PieChartComponent />
            <p className="weight"> Your weight <br/> 60 K</p>
            <p className="Fit-weight">Fit weight <br/> 65 K</p>
            <p className="Fats">Fats  <br/> 12 K</p>
          </div>
        </Box>
      </Container>
      <Container>
        <Box
          sx={{
            flexGrow: 1,
            display: "flex",
            height: 260,
            borderRadius: 5,
            width: 590,
            marginTop: 9,
            marginLeft: 45,
            boxShadow: 10,
          }}
        >
          <h3 className="Activity">Activity</h3>
          <div className="pie2">
            <BarChartComponent />
          </div>
        </Box>
      </Container>
      <Container>
        <Box
          sx={{
            flexGrow: 1,
            display: "flex",
            height: 280,
            borderRadius: 5,
            width: 420,
            marginTop: -73,
            marginLeft: 110,
            boxShadow: 10,
          }}
        >
          <h3 className="Sweat">Sweat</h3>
          <div className="cardsintab">
            <div className="card1intab">
              <MultiActionAreaCard  />
            </div>
            <div className="card2intab">
              {" "}
              <MultiActionAreaCard2 />
            </div>
            <div className="card3intab">
              <MultiActionAreaCard3 />
            </div>
          </div>
        </Box>
      </Container>
    
      <Card
        sx={{
          display: "flex",
          width: 350,
          height: 250,
          marginTop: -33,
          marginLeft: 78,
          borderRadius: 5,
          boxShadow: 10,
        }}
        className="arch"
      >
        <CardMedia component="img" sx={{ width: 160 }} src={ach} />
        <Box sx={{ display: "flex", flexDirection: "column", with: 300 }}>
          <CardContent sx={{ flex: "1 0 auto" }}>
            <Typography component="div" variant="h6">
              Bicep Train : <Percent />{" "}
            </Typography>
            <Typography component="div" variant="h6">
              Tricep Train : <Percent />
            </Typography>
            <Typography component="div" variant="h6">
              Leg Train : <Percent />
            </Typography>
          </CardContent>
        </Box>
       
      </Card>
      <h3 className="Ahcievment">Ahcievment</h3>
      
    </div>
  );
};

export default HomeTab;
