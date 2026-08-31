import { ResponsiveBar } from '@nivo/bar'
/*
import Typography from '@mui/material/Typography'
import Paper from '@mui/material/Paper'


import { nivoDarkTheme, nivoLightTheme } from './SharedConstants'
*/
import data from '../data/expected_points.json'

function ExpectedPointsBarChart(props) {
    var processedData = []

    for (var user in data) {
        processedData.push({
            user: user,
            value1: data[user][0],
            value2: data[user][1]
        })
    }

    return (
        <div style={{ height: '30em' }}>
            <ResponsiveBar
                data={processedData}
                keys={['value1', 'value2']}
                indexBy="user"
                groupMode="grouped"
                margin={{ top: 10, right: 20, bottom: 60, left: 100 }}
                colors={['#4dabf7', '#ff922b']}
                yScale={{
                    type: 'linear',
                    min: 0,
                    max: 'auto'
                }}
                enableLabel={false}
            />
        </div>
    )
}


/*
function ExpectedPointsBarChart(props) {
    var processedData = []

    for (var user in data) {
    processedData.push({
        user: user,
        expectedPoints: data[user][0],
        points: data[user][1]
    })
}

    return (
        <div style={{ height: '30em' }}>
            <ResponsiveBar
                theme={props.darkModeEnabled ? nivoDarkTheme : nivoLightTheme}
                data={processedData}
                keys={['expectedPoints', 'points']}
                indexBy="user"
                groupMode="grouped"

                margin={{ top: 10, right: 180, bottom: 60, left: 100 }}

                colors={({ id }) => {
                    if (id === 'expectedPoints') return '#4dabf7'
                    if (id === 'points') return '#ff922b'
                    return '#999'
                }}

                yScale={{
                    type: 'linear',
                    min: 'auto',
                    max: 'auto'
                }}

                valueFormat={value =>
                    `${Number(value).toLocaleString('de-DE')} €`
                }

                axisLeft={{
                    legend: 'Points',
                    legendOffset: 0,
                    format: value =>
                        new Intl.NumberFormat('de-DE', {
                            maximumFractionDigits: 0,
                            notation: 'compact',
                            compactDisplay: 'short'
                        }).format(value)
                }}

                axisBottom={{
                    legend: 'Manager'
                }}

                enableLabel={false}

                legends={[
    {
        dataFrom: 'keys',
        anchor: 'right',
        direction: 'column',
        translateX: 150,
        itemWidth: 130,
        itemHeight: 20,
        itemsSpacing: 4,
        symbolSize: 20
    }
]}

                tooltip={({ id, value, indexValue, color }) => (
                    <Paper elevation={3} sx={{ padding: 1 }}>
                        <Typography
                            style={{
                                color: color,
                                fontWeight: 'bold'
                            }}
                        >
                            {indexValue}
                        </Typography>

                        <Typography>
                            {id === 'firstValue' ? 'First Value' : 'Second Value'}:
                            {' '}
                            {Number(value).toLocaleString('de-DE')} €
                        </Typography>
                    </Paper>
                )}
            />
        </div>
    )
}
*/

export default ExpectedPointsBarChart