import * as React from "react";
import { useTheme } from "@mui/material/styles";
import Box from "@mui/material/Box";
import Card from "@mui/material/Card";
import CardContent from "@mui/material/CardContent";
import CardMedia from "@mui/material/CardMedia";
import Typography from "@mui/material/Typography";
import fit from "./fit.png";
import { Button, CardActions } from "@mui/material";
import "./css code/card2.css";
import { Link } from "react-router-dom";

export default function MediaControlCard2() {
  const theme = useTheme();

  return (
    <Card sx={{ display: "flex", width: 370, height: 80 }} className="card2">
      <CardMedia
        component="img"
        sx={{ width: 100 }}
        src={fit}
        alt="Fitness Trains"
      />
      <Box sx={{ display: "flex", flexDirection: "column", with: 300 }}>
        <CardContent sx={{ flex: "1 0 auto" }}>
          <Typography component="div" variant="h5">
            Yoga Trains
          </Typography>
          <Typography
            variant="subtitle1"
            color="text.secondary"
            component="div"
          >
            Train Like A pro
          </Typography>
        </CardContent>
      </Box>
      <CardActions className="start2">
        <Link to="./Yoga">start</Link>
      </CardActions>
    </Card>
  );
}
