import { ResponsiveBar } from '@nivo/bar'

import data from '../data/events.json'

function GoalsBarChart(props) {
    var processedData = []

    for (var user in data) {
        processedData.push({
            user: user,
            "Tore/Elfmeter": data[user]["1"] || 0,
            "Assist": data[user]["3"] || 0,
            "Eigentor": data[user]["2"] || 0,
            "Elfer Gehalten": data[user]["7"] || 0
        })
    }

    return (
        <div style={{ height: '30em' }}>
            <ResponsiveBar
                animate={false}
                data={processedData}
                keys={['Tore/Elfmeter', 'Assist',"Elfer Gehalten", 'Eigentor']}
                indexBy="user"
                groupMode="grouped"
                margin={{ top: 10, right: 20, bottom: 60, left: 100 }}
                colors={['#1b569e', '#008cc5', '#00c1d8',"#5df5de"]}
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

export default GoalsBarChart

