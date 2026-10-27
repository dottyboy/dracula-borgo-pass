shader_type spatial;
render_mode cull_back;
// Organic ground: grass blended with bare earth by noise, worn dirt paths between the places the player goes,
// darker patches and a soft fade into the far ground colour at the edge of the terrain mesh.
uniform sampler2D grass_tex : source_color, repeat_enable, filter_linear_mipmap_anisotropic;
uniform sampler2D dirt_tex : source_color, repeat_enable, filter_linear_mipmap_anisotropic;
uniform sampler2D grass_nrm : hint_normal, repeat_enable, filter_linear_mipmap_anisotropic;
uniform vec4 grass_tint : source_color = vec4(1.0);
uniform vec4 dirt_tint : source_color = vec4(1.0);
uniform vec4 far_color : source_color = vec4(0.1, 0.12, 0.1, 1.0);
uniform float grass_scale = 0.25;
uniform float dirt_scale = 0.33;
uniform vec4 rect;                 // playable rectangle: x0, z0, x1, z1
uniform float fade_start = 8.0;
uniform float fade_len = 6.0;
uniform float bare = 0.15;         // 0 = lush meadow ... 1 = mostly bare earth
uniform int path_count = 0;
uniform vec4 path_a[48];           // segment start (x, z) in .xy, end (x, z) in .zw
uniform float path_width = 0.9;
uniform float shore = 0.0;         // 1 = sand and wet stones where the ground dips toward the sea

varying vec3 wpos;
varying float wup;                 // how upright the surface is (1 = flat ground)

float hash(vec2 p) { return fract(sin(dot(p, vec2(127.1, 311.7))) * 43758.5453); }
float noise(vec2 p) {
	vec2 i = floor(p);
	vec2 f = fract(p);
	f = f * f * (3.0 - 2.0 * f);
	return mix(mix(hash(i), hash(i + vec2(1, 0)), f.x), mix(hash(i + vec2(0, 1)), hash(i + vec2(1, 1)), f.x), f.y);
}
float fbm(vec2 p) { return noise(p) * 0.5 + noise(p * 2.1) * 0.3 + noise(p * 4.7) * 0.2; }

float seg_dist(vec2 p, vec2 a, vec2 b) {
	vec2 ab = b - a;
	float t = clamp(dot(p - a, ab) / max(dot(ab, ab), 0.0001), 0.0, 1.0);
	return length(p - (a + ab * t));
}

void vertex() {
	wpos = (MODEL_MATRIX * vec4(VERTEX, 1.0)).xyz;
	wup = normalize((MODEL_MATRIX * vec4(NORMAL, 0.0)).xyz).y;
}

void fragment() {
	vec2 p = wpos.xz;
	float wob = (fbm(p * 0.7) - 0.5) * 0.9;
	float path = 0.0;
	for (int i = 0; i < 48; i++) {
		if (i >= path_count) { break; }
		float d = seg_dist(p, path_a[i].xy, path_a[i].zw) + wob * 0.6;
		path = max(path, 1.0 - smoothstep(path_width * 0.55, path_width * 1.15, d));
	}
	float patches = smoothstep(0.68 - bare * 0.32, 0.82 - bare * 0.32, fbm(p * 0.22 + 7.0));
	float worn = clamp(path + patches * 0.85, 0.0, 1.0);
	vec3 g = texture(grass_tex, p * grass_scale).rgb * grass_tint.rgb;
	g *= 0.82 + 0.36 * fbm(p * 0.35 + 3.0);
	vec3 d = texture(dirt_tex, p * dirt_scale).rgb * dirt_tint.rgb;
	vec3 col = mix(g, d, worn);
	// steep slopes (cliffs, banks) show layered rock instead of grass
	float rock = smoothstep(0.88, 0.66, wup);
	if (rock > 0.0) {
		float strata = fbm(vec2(p.x * 0.25 + p.y * 0.2, wpos.y * 2.4));
		vec3 stone = mix(vec3(0.36, 0.33, 0.29), vec3(0.2, 0.19, 0.18), strata) * (0.85 + 0.3 * fbm(p * 1.9));
		col = mix(col, stone, rock);
	}
	if (shore > 0.5) {
		float sandy = smoothstep(-0.05, -0.55, wpos.y);
		vec3 sand = mix(vec3(0.62, 0.55, 0.40), vec3(0.28, 0.27, 0.25), smoothstep(-0.5, -2.2, wpos.y)) * (0.9 + 0.2 * fbm(p * 1.3));
		col = mix(col, sand, sandy);
	}
	// edge: distance outside the playable rectangle -> far ground colour
	vec2 outside = max(vec2(rect.x - p.x, rect.y - p.y), max(vec2(p.x - rect.z, p.y - rect.w), vec2(0.0)));
	float od = length(outside);
	col = mix(col, far_color.rgb, smoothstep(fade_start, fade_start + fade_len, od + wob * 2.0));
	ALBEDO = col;
	NORMAL_MAP = texture(grass_nrm, p * grass_scale).rgb;
	NORMAL_MAP_DEPTH = 0.6 * (1.0 - worn);
	ROUGHNESS = 1.0;
}
