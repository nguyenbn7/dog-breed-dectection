import { PUBLIC_BASE_API } from '$env/static/public';

/** @type {import('./$types').LayoutLoad} */
export async function load({ fetch }) {
    fetch(PUBLIC_BASE_API);
}