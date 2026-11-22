// Reference implementation of the deployed private training-data storage routes.
// The hosting platform supplies the owner-private service boundary and BUCKET R2 binding.
// Keep PUT private; do not publish this write endpoint without authentication.
function json(value,status=200){return new Response(JSON.stringify(value),{status,headers:{"content-type":"application/json; charset=utf-8","cache-control":"no-store","x-content-type-options":"nosniff"}})}
const TRAINING_DATA_SHA256 = "ddef9fbb3835bb981395cc1c77b904d27e899f8f4c75ac97028be31bb5206682";
const TRAINING_DATA_KEY = `panel-${TRAINING_DATA_SHA256}.csv`;
const MAX_TRAINING_DATA_BYTES = 30 * 1024 * 1024;
function trainingDataManifest(object) {
 return {provider:"cloudflare-r2",key:TRAINING_DATA_KEY,sha256:object.customMetadata?.sha256,size:object.size,version:object.version,etag:object.httpEtag || object.etag};
}
function trainingDataHeaders(object) {
 const headers=new Headers({"content-type":"text/csv; charset=utf-8","cache-control":"private, no-store","x-content-type-options":"nosniff","x-storage-provider":"cloudflare-r2","x-data-sha256":TRAINING_DATA_SHA256,"x-training-data-sha256":TRAINING_DATA_SHA256,"x-object-sha256":TRAINING_DATA_SHA256,"x-object-key":TRAINING_DATA_KEY});
 if(object.version)headers.set("x-object-version",object.version);
 if(object.httpEtag)headers.set("etag",object.httpEtag);
 else if(object.etag)headers.set("etag",`"${object.etag}"`);
 if(Number.isSafeInteger(object.size))headers.set("content-length",String(object.size));
 return headers;
}
function validStoredTrainingData(object) {
 return object?.customMetadata?.sha256===TRAINING_DATA_SHA256 && Number.isSafeInteger(object.size) && object.size>0 && object.size<=MAX_TRAINING_DATA_BYTES;
}
async function trainingDataRoute(request,env,path) {
 const isPanel=path==="/training-data/panel.csv",isManifest=path==="/training-data/manifest.json";
 if(!isPanel&&!isManifest)return null;
 if(request.method!=="GET"&&!(isPanel&&request.method==="PUT")){
  const response=json({error:"Method not allowed"},405);response.headers.set("allow",isPanel?"GET, PUT":"GET");return response;
 }
 const bucket=env?.BUCKET;
 if(!bucket)return json({error:"Training-data cloud storage is not bound"},503);
 if(request.method==="GET"){
  const object=isManifest?await bucket.head(TRAINING_DATA_KEY):await bucket.get(TRAINING_DATA_KEY);
  if(!object)return json({error:"Training dataset has not been uploaded to R2"},404);
  if(!validStoredTrainingData(object))return json({error:"Stored dataset metadata does not match the pinned snapshot"},409);
  if(isManifest)return json(trainingDataManifest(object));
  return new Response(object.body,{headers:trainingDataHeaders(object)});
 }
 const claimedLength=request.headers.get("content-length");
 if(claimedLength!==null&&(!/^\d+$/.test(claimedLength)||Number(claimedLength)>MAX_TRAINING_DATA_BYTES))return json({error:"Training dataset exceeds the 30 MiB size limit or has an invalid length"},413);
 const reader=request.body?.getReader();
 if(!reader)return json({error:"Upload the pinned CSV bytes"},400);
 const chunks=[];let length=0;
 try{
  while(true){const {done,value}=await reader.read();if(done)break;length+=value.byteLength;if(length>MAX_TRAINING_DATA_BYTES){await reader.cancel();return json({error:"Training dataset exceeds the 30 MiB size limit"},413);}chunks.push(value);}
 }finally{reader.releaseLock();}
 if(!length)return json({error:"Upload the pinned CSV bytes"},400);
 const bytes=new Uint8Array(length);let offset=0;for(const chunk of chunks){bytes.set(chunk,offset);offset+=chunk.byteLength;}chunks.length=0;
 const digest=await crypto.subtle.digest("SHA-256",bytes);
 const actualHash=Array.from(new Uint8Array(digest),value=>value.toString(16).padStart(2,"0")).join("");
 if(actualHash!==TRAINING_DATA_SHA256)return json({error:"CSV SHA-256 does not match the pinned cleaned training snapshot",expected_sha256:TRAINING_DATA_SHA256},422);
 const existing=await bucket.get(TRAINING_DATA_KEY);
 if(existing){
  if(!validStoredTrainingData(existing)||existing.size!==length)return json({error:"An incompatible immutable object already exists"},409);
  return json({...trainingDataManifest(existing),already_exists:true});
 }
 const object=await bucket.put(TRAINING_DATA_KEY,bytes,{onlyIf:new Headers({"If-None-Match":"*"}),sha256:digest,customMetadata:{sha256:TRAINING_DATA_SHA256,dataset:"main-street-cleaned-cbp-panel",schema:"panel-v1"},httpMetadata:{contentType:"text/csv; charset=utf-8",cacheControl:"private, no-store"}});
 if(!object){
  const raced=await bucket.head(TRAINING_DATA_KEY);
  if(validStoredTrainingData(raced)&&raced.size===length)return json({...trainingDataManifest(raced),already_exists:true});
  return json({error:"Conditional upload did not create a compatible object"},409);
 }
 if(!validStoredTrainingData(object)||object.size!==length)return json({error:"Uploaded object metadata failed verification"},502);
 return json({...trainingDataManifest(object),already_exists:false},201);
}

export default {async fetch(request,env){
 const path=new URL(request.url).pathname;
 return await trainingDataRoute(request,env,path) || json({error:"Not found"},404);
}};
