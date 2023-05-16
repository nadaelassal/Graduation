import React from 'react'
import PieChartComponent from './bichart';
import BarChartComponent from './barcharts';
const Guides = () =>  {
    return (
        <div>
            <h1>This is the guides page</h1>
            <PieChartComponent/>
            <BarChartComponent/>
        </div>
    )
}

export default Guides;