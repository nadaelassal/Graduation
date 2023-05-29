import React from "react";
import { LineChart, Line, CartesianGrid,XAxis, Tooltip, Legend } from "recharts";

const chartData = [
  { name: "Day 1", value: 100, color: "#FF6384" },
  { name: "Day 2", value: 120, color: "#36A2EB" },
  { name: "Day 3", value: 90, color: "#FFCE56" },
  { name: "Day 4", value: 80, color: "#FF9F40" },
  { name: "Day 5", value: 110, color: "#4BC0C0" },
  { name: "Day 6", value: 70, color: "#9966FF" },
  { name: "Day 7", value: 130, color: "#FF00FF" },
];

const BarChartComponent = () => {
  return (
    <div>
      <div style={{ margin: "20px" }}>
        <LineChart width={550} height={250} data={chartData}>
          <CartesianGrid strokeDasharray="0" vertical={false} />
          <Tooltip />
          <XAxis dataKey="name" />

          <Legend />
          <Line type="monotone" dataKey="value" stroke="#8884d8" />
          {chartData.map((data, index) => (
            <Line
              key={index}
              type="monotone"
              data={data}
              dataKey="value"
              stroke={data.color}
            />
          ))}
        </LineChart>
      </div>
    </div>
  );
};

export default BarChartComponent;
