import React from 'react';
import Box from '@material-ui/core/Box';
import CircularProgress from '@material-ui/core/CircularProgress';

export default function Percent() {

const [uploadOrDownloadCount,
		setUploadOrDownloadCount] = React.useState(10);

React.useEffect(() => {
	const timer = setInterval(() => {
	setUploadOrDownloadCount(
		(beforeValue) => (beforeValue >= 100 ? 0
						: beforeValue + 10));
	}, 800);
	return () => {
	clearInterval(timer);
	};
}, []);

return (
	<div>
	<Box position="relative" display="inline-flex">
		<CircularProgress variant="determinate"
						value={uploadOrDownloadCount} />
		<Box
		bottom={0}
		right={0}
		top={0}
		justifyContent="center"
		left={0}
		display="flex"
		alignItems="center"
		position="absolute"
		>
		{`${Math.round(uploadOrDownloadCount)}%`}
		</Box>
	</Box>
	</div>
);
}
