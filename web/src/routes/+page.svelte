<script>
	let useURL = false;

	/**
	 * @type {HTMLInputElement}
	 */
	let inputFile;
	/**
	 * @type {HTMLImageElement}
	 */
	let uploadImage;
	/**
	 * @type {string | undefined}
	 */
	let imageUrl;
	let errorMessage = '';

	/**
	 * @param {Event & { currentTarget: EventTarget & HTMLInputElement }} $event
	 */
	function onFileSelected($event) {
		const imageFiles = $event.currentTarget.files;
		if (!imageFiles) return;

		var selectedFile = imageFiles[0];
		var reader = new FileReader();

		uploadImage.title = selectedFile.name;

		// @ts-ignore
		reader.onload = function (/**@type {Event & { target: FileReader; }}*/ ev) {
			// @ts-ignore
			uploadImage.src = ev.target.result;
		};

		reader.readAsDataURL(selectedFile);
	}

	/**
	 * @param {string} url
	 */
	function isImageURL(url) {
		return url.match(/\.(jpeg|jpg|gif|png)$/) != null;
	}

	/**
	 * @param {Event & { currentTarget: EventTarget & HTMLInputElement; }} $event
	 */
	function previewImageUrl($event) {
		if (!isImageURL($event.currentTarget.value)) {
			errorMessage = 'Invalid Url';
			return;
		}
		imageUrl = $event.currentTarget.value;
	}

	$: if (useURL) {
		uploadImage.src = '';
	} else {
		imageUrl = '';
	}
</script>

<div class="cover-container d-flex w-100 p-3 flex-column mt-4">
	<div class="">
		<p class="lead">
			<span class="text-warning">
				<span class="fw-bold">WARNING: </span>
				<span class="fst-italic">
					If you upload an image not a dog, machine can not detect it correctly
				</span>
			</span>
		</p>
		<h1>Which breed is that dog</h1>
	</div>

	<main class="w-100 h-100 mt-3 row">
		<div class="col-8">
			<ul class="nav nav-tabs mb-1">
				<li class="nav-item">
					<a
						class="nav-link"
						href={'#'}
						class:active={!useURL}
						on:click={() => {
							useURL = false;
						}}
					>
						Image
					</a>
				</li>
				<li class="nav-item">
					<a
						class="nav-link"
						href={'#'}
						class:active={useURL}
						on:click={() => {
							useURL = true;
						}}
					>
						Link
					</a>
				</li>
			</ul>
			{#if useURL}
				<div class="mt-2 mb-4 input-group">
					<input
						type="text"
						name="Image URL"
						class="form-control me-1"
						placeholder="https://example.com/dog_image.(jpg | png)"
						on:input={previewImageUrl}
					/>
					<button class="btn btn-primary px-4 p-2" disabled={!imageUrl}>Detect</button>
				</div>
				<div class="w-100 h-75 position-relative mt-2">
					{#if imageUrl}
						<!-- svelte-ignore a11y-missing-attribute -->
						<img class="img-fluid" src={imageUrl} />
					{:else}
						<div
							class="border border-white border-opacity-50 rounded border-2 h-100"
							style="--bs-border-style: dashed;"
						></div>
						<p class="position-absolute top-50 start-50 translate-middle">
							{#if errorMessage}
								{errorMessage}
							{:else}
								Preview your image
							{/if}
						</p>
					{/if}
				</div>
			{:else}
				<!-- svelte-ignore a11y-click-events-have-key-events -->
				<!-- svelte-ignore a11y-no-static-element-interactions -->
				<!-- svelte-ignore a11y-click-events-have-key-events -->
				<div class="w-100 h-75 position-relative mt-2">
					<input
						type="file"
						name="file"
						accept="image/png, image/jpeg"
						style="display: none;"
						bind:this={inputFile}
						on:change={onFileSelected}
					/>
					{#if !uploadImage?.src}
						<div
							class="border border-white w-100 h-100 border-opacity-50 rounded border-2"
							style="--bs-border-style: dashed; cursor: pointer;"
							on:click={() => inputFile.click()}
						></div>
						<p class="position-absolute top-50 start-50 translate-middle">
							<i class="fa-solid fa-upload me-2"></i> Upload your image
						</p>
					{:else}
						<button class="btn btn-primary p-2 w-100 mb-4">Detect</button>
					{/if}
					<!-- svelte-ignore a11y-missing-attribute -->
					<!-- svelte-ignore a11y-no-noninteractive-element-interactions -->
					<img
						class="img-fluid"
						bind:this={uploadImage}
						on:click={() => inputFile.click()}
						style="cursor: pointer;"
					/>
				</div>
			{/if}
		</div>
		<div class="col-4 p-0">
			<table class="mb-3">
				<tbody>
					<tr>
						<th scope="row" class="text-start">
							<span class="text-success fw-bold">Best match:</span>
						</th>
						<td class="text-end">Golden Retriever</td>
					</tr>
					<tr>
						<th scope="row" class="text-start">
							<span class="text-info">Confidence score:</span>
						</th>
						<td class="text-end">80%</td>
					</tr>
				</tbody>
			</table>

			<table class="table table-hover table-dark table-sm caption-top">
				<caption class="text-white fw-semibold">Top 5 predictions</caption>
				<thead>
					<tr>
						<th scope="col">#</th>
						<th scope="col">Breed</th>
						<th scope="col">Confidence</th>
					</tr>
				</thead>
				<tbody>
					<tr>
						<th scope="row">1</th>
						<td>Chihuahua</td>
						<td>1%</td>
					</tr>
					<tr>
						<th scope="row">2</th>
						<td>Golden Retriever</td>
						<td>10%</td>
					</tr>
					<tr>
						<th scope="row">3</th>
						<td>Shibainu</td>
						<td>0.01</td>
					</tr>
				</tbody>
			</table>
			<!-- <div class="border border-white h-75"></div> -->
		</div>
	</main>
</div>

<style lang="scss">
	.cover-container {
		max-width: 52em;
	}
</style>
