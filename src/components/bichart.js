import React from "react";
import { PieChart, Pie, Cell } from "recharts";

const COLORS = ["#FF6384", "#36A2EB"];

const data = [
  { name: "weight", value: 20 },
  { name: "fats", value: 50 },
];

const PieChartComponent = () => {
  return (
    
    <PieChart width={300} height={300} className="piechart" >
      <Pie
        data={data}
        dataKey="value"
        nameKey="name"
        cx="50%"
        cy="50%"
        outerRadius={90}
        fill="#8884d8"
      >
        {data.map((entry, index) => (
          <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
        ))}
      </Pie>
    </PieChart>
    
  );
};

export default PieChartComponent;
