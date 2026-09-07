
import { ResponsiveBar } from '@nivo/bar'

import data from '../data/events.json'

function CardsBarChart(props) {
    var processedData = []

    for (var user in data) {
        processedData.push({
            user: user,
            "Gelbe Karten": data[user]["4"] || 0,
            "Gelbrote Karten": data[user]["5"] || 0,
            "Rote Karten": data[user]["6"] || 0
        })
    }

    return (
        <div style={{ height: '30em' }}>
            <ResponsiveBar
                animate={false}
                data={processedData}
                keys={['Gelbe Karten', 'Gelbrote Karten', 'Rote Karten']}
                indexBy="user"
                groupMode="grouped"
                margin={{ top: 10, right: 20, bottom: 60, left: 100 }}
                colors={['#FFD700', '#FFA500', '#FF0000']}
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

export default CardsBarChart

