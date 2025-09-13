import { json } from '@sveltejs/kit';

export async function POST({request}) {
    try {
        const res = await fetch('https://api.ipify.org?format=json');
        const data = await res.json();
        const response = json(data);
        return response;
        
    } catch (error) {
        console.error('Error:', error);
        return json({ error: 'An error while querying ip.' }, { status: 500 });
    }
}
