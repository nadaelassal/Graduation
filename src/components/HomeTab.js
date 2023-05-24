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
            height: 270,
            borderRadius: 25,
            width: 320,
            marginLeft: 2,
            marginTop: -75,
            boxShadow: 10,
          }}
        >
          <h3 className="BMI">BMI </h3>
          <div className="pie">
            <PieChartComponent />
          </div>
        </Box>
      </Container>
      <Container>
        <Box
          sx={{
            flexGrow: 1,
            display: "flex",
            height: 315,
            borderRadius: 25,
            width: 650,
            marginTop: 3.5,
            marginLeft: 30,
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
            borderRadius: 25,
            width: 480,
            marginTop: -75,
            marginLeft: 100,
            boxShadow: 10,
          }}
        >
          <h3 className="Sweat">Sweat</h3>
          <div className="cardsintab">
            <div className="card1intab">
              <MultiActionAreaCard />
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
          width: 370,
          height: 270,
          marginTop: -37,
          marginLeft: 68,
          borderRadius: 25,
          boxShadow: 10,
        }}
        className="arch"
      >
        <CardMedia component="img" sx={{ width: 160 }} src={ach} />
        <Box sx={{ display: "flex", flexDirection: "column", with: 300 }}>
          <CardContent sx={{ flex: "1 0 auto" }}>
            <Typography component="div" variant="h5">
              Bicep Train : <Percent />{" "}
            </Typography>
            <Typography component="div" variant="h5">
              Tricep Train : <Percent />
            </Typography>
            <Typography component="div" variant="h5">
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
